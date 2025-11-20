"""
Vistas de reportes.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from apps.loans.models import Loan
from apps.payments.models import Payment
from apps.users.models import UserProfile
from apps.reports.services import ReportService
from apps.reports.exporters import PDFExporter, ExcelExporter
from apps.authentication.decorators import tenant_required


@tenant_required
@login_required
def reports_dashboard_view(request):
    """
    Dashboard de reportes.
    """
    tenant = request.user.tenant
    
    # Estadísticas generales
    stats = ReportService.get_dashboard_stats(tenant)
    
    # Préstamos por estado
    loans_by_status = list(Loan.objects.filter(tenant=tenant).values('status').annotate(
        count=Count('id'),
        total=Sum('amount')
    ))
    
    # Si no hay datos, crear estructura vacía
    if not loans_by_status:
        loans_by_status = [
            {'status': 'ACTIVO', 'count': 0, 'total': 0},
            {'status': 'COMPLETADO', 'count': 0, 'total': 0},
            {'status': 'VENCIDO', 'count': 0, 'total': 0},
        ]
    
    # Pagos por mes (últimos 6 meses)
    six_months_ago = datetime.now() - timedelta(days=180)
    payments_by_month = list(Payment.objects.filter(
        loan__tenant=tenant,
        status='COMPLETADO',
        payment_date__gte=six_months_ago
    ).extra(
        select={'month': "DATE_TRUNC('month', payment_date)"}
    ).values('month').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month'))
    
    # Si no hay datos, crear estructura vacía
    if not payments_by_month:
        payments_by_month = []
    
    # Top prestatarios
    top_borrowers = ReportService.get_top_borrowers(tenant, limit=5)
    
    # Distribución de préstamos por rango de monto
    from decimal import Decimal
    all_loans = Loan.objects.filter(tenant=tenant)
    amount_ranges = {
        'range_0_1000': all_loans.filter(amount__lte=Decimal('1000')).count(),
        'range_1000_5000': all_loans.filter(amount__gt=Decimal('1000'), amount__lte=Decimal('5000')).count(),
        'range_5000_10000': all_loans.filter(amount__gt=Decimal('5000'), amount__lte=Decimal('10000')).count(),
        'range_10000_plus': all_loans.filter(amount__gt=Decimal('10000')).count(),
    }
    
    context = {
        'stats': stats,
        'loans_by_status': loans_by_status,
        'payments_by_month': payments_by_month,
        'top_borrowers': top_borrowers,
        'amount_ranges': amount_ranges,
    }
    
    return render(request, 'reports/dashboard.html', context)


@tenant_required
@login_required
def loans_report_view(request):
    """
    Reporte de préstamos.
    """
    tenant = request.user.tenant
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    loans = Loan.objects.filter(tenant=tenant)
    
    if start_date:
        loans = loans.filter(created_at__gte=start_date)
    if end_date:
        loans = loans.filter(created_at__lte=end_date)
    
    context = {
        'loans': loans.order_by('-created_at'),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reports/loans_report.html', context)


@tenant_required
@login_required
def export_loans_report_pdf(request):
    """
    Exporta reporte de préstamos a PDF.
    """
    tenant = request.user.tenant
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    loans = Loan.objects.filter(tenant=tenant)
    
    if start_date:
        loans = loans.filter(created_at__gte=start_date)
    if end_date:
        loans = loans.filter(created_at__lte=end_date)
    
    loans = loans.order_by('-created_at')
    
    filename = f'reporte_prestamos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    return PDFExporter.export_loans_pdf(loans, filename)


@tenant_required
@login_required
def export_payments_report_pdf(request):
    """
    Exporta reporte de pagos a PDF.
    """
    tenant = request.user.tenant
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    payments = Payment.objects.filter(loan__tenant=tenant, status='COMPLETADO')
    
    if start_date:
        payments = payments.filter(payment_date__gte=start_date)
    if end_date:
        payments = payments.filter(payment_date__lte=end_date)
    
    payments = payments.order_by('-payment_date')
    
    filename = f'reporte_pagos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    return PDFExporter.export_payments_pdf(payments, filename)


@tenant_required
@login_required
def payments_report_view(request):
    """
    Reporte de pagos.
    """
    tenant = request.user.tenant
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    payments = Payment.objects.filter(loan__tenant=tenant, status='COMPLETADO')
    
    if start_date:
        payments = payments.filter(payment_date__gte=start_date)
    if end_date:
        payments = payments.filter(payment_date__lte=end_date)
    
    context = {
        'payments': payments.order_by('-payment_date'),
        'total_amount': payments.aggregate(total=Sum('amount'))['total'] or 0,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reports/payments_report.html', context)
