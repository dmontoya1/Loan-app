"""
Vistas de pagos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from .models import Payment
from .forms import PaymentForm
from .services import PaymentService
from apps.authentication.mixins import TenantRequiredMixin
from apps.reports.exporters import PDFExporter, ExcelExporter
from datetime import datetime


class PaymentListView(TenantRequiredMixin, ListView):
    """
    Lista de pagos.
    """
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        loan_id = self.request.GET.get('loan', '')
        
        if search:
            queryset = queryset.filter(
                Q(loan__user_profile__first_name__icontains=search) |
                Q(loan__user_profile__last_name__icontains=search) |
                Q(loan__user_profile__document_number__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if loan_id:
            queryset = queryset.filter(loan_id=loan_id)
        
        return queryset.order_by('-due_date', 'payment_number')


class PaymentUpdateView(TenantRequiredMixin, UpdateView):
    """
    Actualizar pago (marcar como completado).
    """
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'
    success_url = reverse_lazy('payments:list')

    def form_valid(self, form):
        if form.cleaned_data.get('status') == 'COMPLETADO' and not form.instance.payment_date:
            form.instance.payment_date = date.today()
        
        messages.success(self.request, f'Pago #{form.instance.payment_number} actualizado exitosamente.')
        return super().form_valid(form)


@login_required
def process_payment_view(request, payment_id):
    """
    Procesa un pago.
    """
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        loan__tenant=request.user.tenant
    )
    
    PaymentService.process_payment(payment_id)
    messages.success(request, f'Pago #{payment.payment_number} procesado exitosamente.')
    
    return redirect('payments:list')


@login_required
def create_payment_view(request, payment_id):
    """
    Crear/procesar un pago rápidamente con fecha actual.
    """
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        loan__tenant=request.user.tenant
    )
    
    if request.method == 'POST':
        payment.mark_as_completed()
        messages.success(request, f'Pago #{payment.payment_number} procesado exitosamente con fecha de hoy.')
        return redirect('payments:list')
    
    # Si es GET, redirigir al formulario de edición
    return redirect('payments:update', pk=payment_id)


@login_required
def overdue_payments_view(request):
    """
    Vista de pagos vencidos.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    overdue_payments = PaymentService.get_overdue_payments(request.user.tenant)
    
    return render(request, 'payments/overdue_list.html', {
        'payments': overdue_payments
    })


@login_required
def export_payments_pdf(request):
    """
    Exporta pagos a PDF.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    payments = Payment.objects.filter(loan__tenant=request.user.tenant)
    
    # Aplicar filtros si existen
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        payments = payments.filter(
            Q(loan__user_profile__first_name__icontains=search) |
            Q(loan__user_profile__last_name__icontains=search) |
            Q(loan__user_profile__document_number__icontains=search)
        )
    
    if status:
        payments = payments.filter(status=status)
    
    payments = payments.order_by('-due_date', 'payment_number')
    
    filename = f'pagos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    return PDFExporter.export_payments_pdf(payments, filename)


@login_required
def export_payments_excel(request):
    """
    Exporta pagos a Excel.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    payments = Payment.objects.filter(loan__tenant=request.user.tenant)
    
    # Aplicar filtros si existen
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        payments = payments.filter(
            Q(loan__user_profile__first_name__icontains=search) |
            Q(loan__user_profile__last_name__icontains=search) |
            Q(loan__user_profile__document_number__icontains=search)
        )
    
    if status:
        payments = payments.filter(status=status)
    
    payments = payments.order_by('-due_date', 'payment_number')
    
    filename = f'pagos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    return ExcelExporter.export_payments_excel(payments, filename)


@login_required
def export_payment_receipt_pdf(request, payment_id):
    """
    Genera un comprobante de pago en PDF.
    """
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        messages.error(request, 'No tienes un tenant asignado.')
        return redirect('authentication:login')
    
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        loan__tenant=request.user.tenant
    )
    
    return PDFExporter.export_payment_receipt_pdf(payment)
