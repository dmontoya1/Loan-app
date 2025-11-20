"""
Servicios para reportes (Service Layer Pattern).
"""
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import datetime, timedelta
from apps.loans.models import Loan
from apps.payments.models import Payment
from apps.users.models import UserProfile


class ReportService:
    """
    Servicio para generar reportes.
    """

    @staticmethod
    def get_dashboard_stats(tenant):
        """
        Obtiene estadísticas del dashboard.
        """
        loans = Loan.objects.filter(tenant=tenant)
        total_loans = loans.count()
        active_loans = loans.filter(status='ACTIVO').count()
        completed_loans = loans.filter(status='COMPLETADO').count()
        overdue_loans = loans.filter(status='VENCIDO').count()

        total_lent = loans.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_paid = Payment.objects.filter(
            loan__tenant=tenant,
            status='COMPLETADO'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        total_users = UserProfile.objects.filter(tenant=tenant, is_active=True).count()

        pending_payments = Payment.objects.filter(
            loan__tenant=tenant,
            status='PENDIENTE'
        ).count()

        overdue_payments = Payment.objects.filter(
            loan__tenant=tenant,
            status='VENCIDO'
        ).count()
        
        completed_payments = Payment.objects.filter(
            loan__tenant=tenant,
            status='COMPLETADO'
        ).count()

        return {
            'total_loans': total_loans,
            'active_loans': active_loans,
            'completed_loans': completed_loans,
            'overdue_loans': overdue_loans,
            'total_lent': total_lent,
            'total_amount': total_lent,  # Alias para compatibilidad
            'total_paid': total_paid,
            'total_pending': total_lent - total_paid,
            'pending_amount': total_lent - total_paid,  # Alias para compatibilidad
            'total_users': total_users,
            'pending_payments': pending_payments,
            'overdue_payments': overdue_payments,
            'completed_payments': completed_payments,
        }

    @staticmethod
    def get_loans_by_period(tenant, start_date, end_date):
        """
        Obtiene préstamos en un rango de fechas.
        """
        return Loan.objects.filter(
            tenant=tenant,
            created_at__range=[start_date, end_date]
        )

    @staticmethod
    def get_payments_by_period(tenant, start_date, end_date):
        """
        Obtiene pagos en un rango de fechas.
        """
        return Payment.objects.filter(
            loan__tenant=tenant,
            payment_date__range=[start_date, end_date],
            status='COMPLETADO'
        )

    @staticmethod
    def get_top_borrowers(tenant, limit=10):
        """
        Obtiene los principales prestatarios.
        """
        return UserProfile.objects.filter(
            tenant=tenant,
            loans__isnull=False
        ).annotate(
            total_loans=Count('loans'),
            total_borrowed=Sum('loans__amount')
        ).order_by('-total_borrowed')[:limit]
