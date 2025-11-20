"""
API Views para reportes.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
from .services import ReportService


@api_view(['GET'])
def dashboard_stats(request):
    """Obtener estadísticas del dashboard."""
    if not request.user.tenant:
        return Response(
            {'error': 'Usuario no tiene tenant asignado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    stats = ReportService.get_dashboard_stats(request.user.tenant)
    
    # Estadísticas adicionales para gráficos
    loans_by_status = {}
    for status_choice in ['ACTIVO', 'COMPLETADO', 'CANCELADO', 'VENCIDO']:
        loans_by_status[status_choice] = request.user.tenant.loans.filter(
            status=status_choice
        ).count()
    
    # Pagos por mes (últimos 6 meses)
    payments_by_month = []
    for i in range(6):
        month_start = (timezone.now() - timedelta(days=30*i)).replace(day=1)
        if i > 0:
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            month_end = timezone.now().date()
        
        payments_count = request.user.tenant.loans.filter(
            payments__status='COMPLETADO',
            payments__payment_date__gte=month_start,
            payments__payment_date__lte=month_end
        ).aggregate(
            count=Count('payments'),
            total=Sum('payments__amount')
        )
        
        payments_by_month.append({
            'month': month_start.strftime('%Y-%m'),
            'count': payments_count['count'] or 0,
            'total': float(payments_count['total'] or 0)
        })
    
    payments_by_month.reverse()
    
    return Response({
        **stats,
        'loans_by_status': loans_by_status,
        'payments_by_month': payments_by_month
    })


@api_view(['GET'])
def loans_report(request):
    """Reporte de préstamos."""
    if not request.user.tenant:
        return Response(
            {'error': 'Usuario no tiene tenant asignado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date and end_date:
        loans = ReportService.get_loans_by_period(
            request.user.tenant,
            start_date,
            end_date
        )
    else:
        loans = request.user.tenant.loans.all()
    
    from apps.loans.serializers import LoanListSerializer
    serializer = LoanListSerializer(loans, many=True)
    
    return Response({
        'loans': serializer.data,
        'total': loans.count(),
        'total_amount': float(loans.aggregate(Sum('amount'))['amount__sum'] or 0)
    })


@api_view(['GET'])
def payments_report(request):
    """Reporte de pagos."""
    if not request.user.tenant:
        return Response(
            {'error': 'Usuario no tiene tenant asignado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date and end_date:
        payments = ReportService.get_payments_by_period(
            request.user.tenant,
            start_date,
            end_date
        )
    else:
        payments = request.user.tenant.loans.filter(
            payments__status='COMPLETADO'
        ).values('payments').distinct()
        from apps.payments.models import Payment
        payment_ids = [p['payments'] for p in payments if p['payments']]
        payments = Payment.objects.filter(id__in=payment_ids)
    
    from apps.payments.serializers import PaymentSerializer
    serializer = PaymentSerializer(payments, many=True)
    
    return Response({
        'payments': serializer.data,
        'total': payments.count(),
        'total_amount': float(payments.aggregate(Sum('amount'))['amount__sum'] or 0)
    })

