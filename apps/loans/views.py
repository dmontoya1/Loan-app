"""
Vistas de préstamos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q
from datetime import datetime
from django.http import JsonResponse
from .models import Loan, LoanTemplate
from .forms import LoanForm, LoanImportForm, LoanTemplateForm
from .services import LoanService, PaymentFactory
from apps.reports.exporters import PDFExporter, ExcelExporter
from apps.authentication.mixins import TenantRequiredMixin
from apps.reports.services import ReportService


class LoanListView(TenantRequiredMixin, ListView):
    """
    Lista de préstamos.
    """
    model = Loan
    template_name = 'loans/loan_list.html'
    context_object_name = 'loans'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        payment_frequency = self.request.GET.get('payment_frequency', '')
        amount_min = self.request.GET.get('amount_min', '')
        amount_max = self.request.GET.get('amount_max', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        
        # Búsqueda mejorada (nombre, documento, email, teléfono)
        if search:
            queryset = queryset.filter(
                Q(user_profile__first_name__icontains=search) |
                Q(user_profile__last_name__icontains=search) |
                Q(user_profile__document_number__icontains=search) |
                Q(user_profile__email__icontains=search) |
                Q(user_profile__phone__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if payment_frequency:
            queryset = queryset.filter(payment_frequency=payment_frequency)
        
        # Filtros avanzados
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)
        
        if date_from:
            queryset = queryset.filter(start_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(start_date__lte=date_to)
        
        return queryset.order_by('-created_at')
    
    def get_export_queryset(self):
        """Retorna el queryset filtrado para exportación."""
        return self.get_queryset()


class LoanCreateView(TenantRequiredMixin, CreateView):
    """
    Crear nuevo préstamo.
    """
    model = Loan
    form_class = LoanForm
    template_name = 'loans/loan_form.html'
    success_url = reverse_lazy('loans:list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        
        # Si se seleccionó una plantilla, aplicar sus valores
        template_id = self.request.POST.get('template', '')
        if template_id:
            try:
                template = LoanTemplate.objects.get(id=template_id, tenant=self.request.user.tenant)
                if not form.cleaned_data.get('amount') and template.amount:
                    form.instance.amount = template.amount
                if not form.cleaned_data.get('total_payments') and template.total_payments:
                    form.instance.total_payments = template.total_payments
                if template.notes:
                    existing_notes = form.cleaned_data.get('notes', '')
                    form.instance.notes = f"{existing_notes}\n\n(Usando plantilla: {template.name})".strip()
            except LoanTemplate.DoesNotExist:
                pass
        
        response = super().form_valid(form)  # Guarda el préstamo
        # Crear los pagos después de guardar
        PaymentFactory.create_payments_for_loan(self.object)
        messages.success(self.request, f'Préstamo #{self.object.id} creado exitosamente con {self.object.total_payments} pagos.')
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.user.tenant
        return kwargs


class LoanImportView(TenantRequiredMixin, CreateView):
    """
    Importar préstamo existente con pagos ya realizados.
    """
    model = Loan
    form_class = LoanImportForm
    template_name = 'loans/loan_import.html'
    success_url = reverse_lazy('loans:list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        response = super().form_valid(form)  # Guarda el préstamo
        
        # Obtener datos del formulario
        payments_completed = form.cleaned_data.get('payments_completed', 0) or 0
        last_payment_date = form.cleaned_data.get('last_payment_date')
        
        # Crear los pagos con los completados marcados
        PaymentFactory.create_payments_for_loan(
            self.object, 
            payments_completed=payments_completed,
            last_payment_date=last_payment_date
        )
        
        messages.success(
            self.request, 
            f'Préstamo #{self.object.id} importado exitosamente. {payments_completed} pagos marcados como completados de {self.object.total_payments} totales.'
        )
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.user.tenant
        return kwargs


class LoanDetailView(TenantRequiredMixin, DetailView):
    """
    Detalle de préstamo.
    """
    model = Loan
    template_name = 'loans/loan_detail.html'
    context_object_name = 'loan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payments.all().order_by('payment_number')
        return context


class LoanUpdateView(TenantRequiredMixin, UpdateView):
    """
    Actualizar préstamo.
    """
    model = Loan
    form_class = LoanForm
    template_name = 'loans/loan_form.html'
    success_url = reverse_lazy('loans:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.user.tenant
        # No mostrar template en edición
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        return kwargs


class LoanDeleteView(TenantRequiredMixin, DeleteView):
    """
    Eliminar préstamo.
    """
    model = Loan
    template_name = 'loans/loan_confirm_delete.html'
    success_url = reverse_lazy('loans:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Préstamo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


@login_required
def dashboard_view(request):
    """
    Dashboard principal.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')

    from apps.payments.services import PaymentService
    from apps.reports.services import ReportService
    from django.db.models import Sum, Count
    import json
    
    stats = ReportService.get_dashboard_stats(request.user.tenant)
    recent_loans = Loan.objects.filter(tenant=request.user.tenant).order_by('-created_at')[:10]
    overdue_payments = PaymentService.get_overdue_payments(request.user.tenant)[:10]
    overdue_count = PaymentService.get_overdue_payments(request.user.tenant).count()
    
    # Pagos próximos a vencer (próximos 7 días)
    from datetime import date, timedelta
    from apps.payments.models import Payment
    next_7_days = date.today() + timedelta(days=7)
    upcoming_payments = Payment.objects.filter(
        loan__tenant=request.user.tenant,
        status='PENDIENTE',
        due_date__lte=next_7_days,
        due_date__gt=date.today()
    ).order_by('due_date')[:10]
    upcoming_count = Payment.objects.filter(
        loan__tenant=request.user.tenant,
        status='PENDIENTE',
        due_date__lte=next_7_days,
        due_date__gt=date.today()
    ).count()
    
    # Datos para gráficos interactivos
    # Préstamos por estado
    loans_by_status = list(Loan.objects.filter(tenant=request.user.tenant).values('status').annotate(
        count=Count('id'),
        total=Sum('amount')
    ))
    if not loans_by_status:
        loans_by_status = [
            {'status': 'ACTIVO', 'count': 0, 'total': 0},
            {'status': 'COMPLETADO', 'count': 0, 'total': 0},
            {'status': 'VENCIDO', 'count': 0, 'total': 0},
        ]
    
    # Pagos por mes (últimos 6 meses)
    six_months_ago = datetime.now() - timedelta(days=180)
    payments_by_month = list(Payment.objects.filter(
        loan__tenant=request.user.tenant,
        status='COMPLETADO',
        payment_date__gte=six_months_ago
    ).extra(
        select={'month': "DATE_TRUNC('month', payment_date)"}
    ).values('month').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month'))
    
    if not payments_by_month:
        payments_by_month = []
    
    # Distribución por rango de monto
    from decimal import Decimal
    all_loans = Loan.objects.filter(tenant=request.user.tenant)
    amount_ranges = {
        'range_0_1000': all_loans.filter(amount__lte=Decimal('1000')).count(),
        'range_1000_5000': all_loans.filter(amount__gt=Decimal('1000'), amount__lte=Decimal('5000')).count(),
        'range_5000_10000': all_loans.filter(amount__gt=Decimal('5000'), amount__lte=Decimal('10000')).count(),
        'range_10000_plus': all_loans.filter(amount__gt=Decimal('10000')).count(),
    }
    
    # Clase personalizada para serializar Decimal a float
    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return super(DecimalEncoder, self).default(obj)

    # Convertir a JSON para JavaScript
    loans_by_status_json = json.dumps(loans_by_status, cls=DecimalEncoder)
    payments_by_month_json = json.dumps(payments_by_month, cls=DecimalEncoder, default=str)
    amount_ranges_json = json.dumps(amount_ranges, cls=DecimalEncoder)

    context = {
        'stats': stats,
        'recent_loans': recent_loans,
        'overdue_payments': overdue_payments,
        'overdue_count': overdue_count,
        'upcoming_payments': upcoming_payments,
        'upcoming_payments_count': upcoming_count,
        'loans_by_status': loans_by_status_json,
        'payments_by_month': payments_by_month_json,
        'amount_ranges': amount_ranges_json,
    }

    return render(request, 'loans/dashboard.html', context)


@login_required
def export_loans_pdf(request):
    """
    Exporta préstamos a PDF.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    loans = Loan.objects.filter(tenant=request.user.tenant)
    
    # Aplicar todos los filtros disponibles
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    payment_frequency = request.GET.get('payment_frequency', '')
    amount_min = request.GET.get('amount_min', '')
    amount_max = request.GET.get('amount_max', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if search:
        loans = loans.filter(
            Q(user_profile__first_name__icontains=search) |
            Q(user_profile__last_name__icontains=search) |
            Q(user_profile__document_number__icontains=search) |
            Q(user_profile__email__icontains=search) |
            Q(user_profile__phone__icontains=search)
        )
    
    if status:
        loans = loans.filter(status=status)
    
    if payment_frequency:
        loans = loans.filter(payment_frequency=payment_frequency)
    
    if amount_min:
        loans = loans.filter(amount__gte=amount_min)
    
    if amount_max:
        loans = loans.filter(amount__lte=amount_max)
    
    if date_from:
        loans = loans.filter(start_date__gte=date_from)
    
    if date_to:
        loans = loans.filter(start_date__lte=date_to)
    
    loans = loans.order_by('-created_at')
    
    filename = f'prestamos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    return PDFExporter.export_loans_pdf(loans, filename)


@login_required
def export_loans_excel(request):
    """
    Exporta préstamos a Excel.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    loans = Loan.objects.filter(tenant=request.user.tenant)
    
    # Aplicar todos los filtros disponibles
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    payment_frequency = request.GET.get('payment_frequency', '')
    amount_min = request.GET.get('amount_min', '')
    amount_max = request.GET.get('amount_max', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if search:
        loans = loans.filter(
            Q(user_profile__first_name__icontains=search) |
            Q(user_profile__last_name__icontains=search) |
            Q(user_profile__document_number__icontains=search) |
            Q(user_profile__email__icontains=search) |
            Q(user_profile__phone__icontains=search)
        )
    
    if status:
        loans = loans.filter(status=status)
    
    if payment_frequency:
        loans = loans.filter(payment_frequency=payment_frequency)
    
    if amount_min:
        loans = loans.filter(amount__gte=amount_min)
    
    if amount_max:
        loans = loans.filter(amount__lte=amount_max)
    
    if date_from:
        loans = loans.filter(start_date__gte=date_from)
    
    if date_to:
        loans = loans.filter(start_date__lte=date_to)
    
    loans = loans.order_by('-created_at')
    
    filename = f'prestamos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    return ExcelExporter.export_loans_excel(loans, filename)


# Vistas para Templates de Préstamos
class LoanTemplateListView(TenantRequiredMixin, ListView):
    """
    Lista de plantillas de préstamos.
    """
    model = LoanTemplate
    template_name = 'loans/loan_template_list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        return LoanTemplate.objects.filter(
            tenant=self.request.user.tenant
        ).order_by('name')


class LoanTemplateCreateView(TenantRequiredMixin, CreateView):
    """
    Crear nueva plantilla de préstamo.
    """
    model = LoanTemplate
    form_class = LoanTemplateForm
    template_name = 'loans/loan_template_form.html'
    success_url = reverse_lazy('loans:templates')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        messages.success(self.request, f'Plantilla "{form.instance.name}" creada exitosamente.')
        return super().form_valid(form)


class LoanTemplateUpdateView(TenantRequiredMixin, UpdateView):
    """
    Editar plantilla de préstamo.
    """
    model = LoanTemplate
    form_class = LoanTemplateForm
    template_name = 'loans/loan_template_form.html'
    success_url = reverse_lazy('loans:templates')

    def form_valid(self, form):
        messages.success(self.request, f'Plantilla "{form.instance.name}" actualizada exitosamente.')
        return super().form_valid(form)


class LoanTemplateDeleteView(TenantRequiredMixin, DeleteView):
    """
    Eliminar plantilla de préstamo.
    """
    model = LoanTemplate
    template_name = 'loans/loan_template_confirm_delete.html'
    success_url = reverse_lazy('loans:templates')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Plantilla eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


@login_required
def get_template_json(request, template_id):
    """
    API endpoint para obtener datos de una plantilla en JSON.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        template = LoanTemplate.objects.get(
            id=template_id,
            tenant=request.user.tenant,
            is_active=True
        )
        return JsonResponse({
            'amount': float(template.amount) if template.amount else None,
            'interest_rate': float(template.interest_rate),
            'payment_frequency': template.payment_frequency,
            'total_payments': template.total_payments,
            'notes': template.notes,
        })
    except LoanTemplate.DoesNotExist:
        return JsonResponse({'error': 'Plantilla no encontrada'}, status=404)