"""
Servicios para préstamos (Service Layer Pattern).
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.db import transaction
from .models import Loan
from apps.payments.models import Payment


class LoanService:
    """
    Servicio para operaciones de préstamos.
    """

    @staticmethod
    def create_loan_with_payments(loan_data):
        """
        Crea un préstamo y sus pagos asociados.
        Usa Factory Pattern para crear los pagos.
        """
        with transaction.atomic():
            # Obtener o crear el préstamo
            if isinstance(loan_data, Loan):
                loan = loan_data
            else:
                loan = Loan.objects.create(**loan_data)

            # Crear los pagos usando el factory
            PaymentFactory.create_payments_for_loan(loan)

            return loan

    @staticmethod
    def calculate_payment_schedule(loan):
        """
        Calcula la fecha de cada pago según la frecuencia.
        """
        schedule = []
        current_date = loan.start_date

        frequency_days = {
            'SEMANAL': 7,
            'QUINCENAL': 15,
            'MENSUAL': 30,
        }

        days_increment = frequency_days.get(loan.payment_frequency, 30)

        for i in range(1, loan.total_payments + 1):
            due_date = current_date + timedelta(days=days_increment * (i - 1))
            schedule.append({
                'payment_number': i,
                'due_date': due_date,
                'amount': loan.payment_amount,
            })

        return schedule


class PaymentFactory:
    """
    Factory para crear pagos (Factory Pattern).
    """

    @staticmethod
    def create_payments_for_loan(loan, payments_completed=0, last_payment_date=None):
        """
        Crea todos los pagos asociados a un préstamo.
        Permite marcar pagos como completados si es una importación.
        
        Args:
            loan: Instancia del préstamo
            payments_completed: Número de pagos que ya fueron completados (default: 0)
            last_payment_date: Fecha del último pago realizado (opcional)
        """
        schedule = LoanService.calculate_payment_schedule(loan)
        payments = []

        for payment_data in schedule:
            payment_number = payment_data['payment_number']
            is_completed = payment_number <= payments_completed if payments_completed else False
            
            # Si está completado y hay fecha, usar la fecha calculada o la última fecha
            payment_date = None
            if is_completed:
                if last_payment_date and payment_number == payments_completed:
                    # Para el último pago completado, usar la fecha proporcionada
                    payment_date = last_payment_date
                else:
                    # Para otros pagos completados, usar la fecha de vencimiento
                    payment_date = payment_data['due_date']

            payment = Payment.objects.create(
                loan=loan,
                amount=payment_data['amount'],
                due_date=payment_data['due_date'],
                payment_number=payment_number,
                status='COMPLETADO' if is_completed else 'PENDIENTE',
                payment_date=payment_date,
            )
            payments.append(payment)

        return payments

    @staticmethod
    def create_payment(loan, payment_number, amount, due_date, status='PENDIENTE', payment_date=None):
        """
        Crea un pago individual.
        
        Args:
            loan: Instancia del préstamo
            payment_number: Número de pago
            amount: Monto del pago
            due_date: Fecha de vencimiento
            status: Estado del pago (default: 'PENDIENTE')
            payment_date: Fecha en que se realizó el pago (opcional)
        """
        return Payment.objects.create(
            loan=loan,
            payment_number=payment_number,
            amount=amount,
            due_date=due_date,
            status=status,
            payment_date=payment_date,
        )
