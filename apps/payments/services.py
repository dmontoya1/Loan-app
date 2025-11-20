"""
Servicios para pagos (Service Layer Pattern).
"""
from decimal import Decimal
from datetime import date
from django.db import transaction
from .models import Payment
from apps.loans.models import Loan


class PaymentService:
    """
    Servicio para operaciones de pagos.
    """

    @staticmethod
    def process_payment(payment_id, payment_date=None):
        """
        Procesa un pago y actualiza el estado del préstamo si es necesario.
        """
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(id=payment_id)
            payment.mark_as_completed(payment_date)

            # Verificar si el préstamo está completo
            loan = payment.loan
            if loan.completed_payments_count >= loan.total_payments:
                loan.status = 'COMPLETADO'
                loan.save()

            return payment

    @staticmethod
    def get_overdue_payments(tenant=None):
        """
        Obtiene todos los pagos vencidos.
        """
        today = date.today()
        queryset = Payment.objects.filter(
            due_date__lt=today,
        ).exclude(status='COMPLETADO')

        if tenant:
            queryset = queryset.filter(loan__tenant=tenant)

        return queryset

    @staticmethod
    def update_overdue_status():
        """
        Actualiza el estado de pagos vencidos.
        """
        overdue_payments = PaymentService.get_overdue_payments()
        overdue_payments.update(status='VENCIDO')

        # Actualizar préstamos con pagos vencidos
        loans_to_update = Loan.objects.filter(
            payments__status='VENCIDO',
            status='ACTIVO',
        ).distinct()

        for loan in loans_to_update:
            if loan.completed_payments_count < loan.total_payments:
                loan.status = 'VENCIDO'
                loan.save()
