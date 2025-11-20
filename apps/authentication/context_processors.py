"""
Context processors para agregar información global a los templates.
"""
from apps.payments.services import PaymentService


def notifications(request):
    """
    Agrega notificaciones globales a todos los templates.
    """
    if not request.user.is_authenticated:
        return {}
    
    if not hasattr(request.user, 'tenant') or not request.user.tenant:
        return {}
    
    try:
        overdue_count = PaymentService.get_overdue_payments(request.user.tenant).count()
        
        # Pagos próximos a vencer (próximos 7 días)
        from datetime import date, timedelta
        from apps.payments.models import Payment
        next_7_days = date.today() + timedelta(days=7)
        upcoming_count = Payment.objects.filter(
            loan__tenant=request.user.tenant,
            status='PENDIENTE',
            due_date__lte=next_7_days,
            due_date__gt=date.today()
        ).count()
        
        return {
            'overdue_payments_count': overdue_count,
            'upcoming_payments_count': upcoming_count,
            'total_notifications': overdue_count + upcoming_count,
        }
    except Exception:
        return {
            'overdue_payments_count': 0,
            'upcoming_payments_count': 0,
            'total_notifications': 0,
        }
