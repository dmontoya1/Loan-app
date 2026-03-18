"""
Loan models.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.authentication.models import Tenant
from apps.users.models import UserProfile


class LoanTemplate(models.Model):
    """
    Plantilla de préstamo para crear préstamos rápidamente.
    """
    PAYMENT_FREQUENCY_CHOICES = [
        ('SEMANAL', 'Semanal'),
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
    ]
    
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='loan_templates',
        verbose_name='Tenant'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre de la Plantilla')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Monto (Opcional)'
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Tasa de Interés (%)'
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        verbose_name='Frecuencia de Pago'
    )
    total_payments = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Número de Pagos (Opcional)'
    )
    notes = models.TextField(blank=True, verbose_name='Notas')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Plantilla de Préstamo'
        verbose_name_plural = 'Plantillas de Préstamos'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.interest_rate}%"


class Loan(models.Model):
    """
    Modelo de préstamo.
    """
    PAYMENT_FREQUENCY_CHOICES = [
        ('SEMANAL', 'Semanal'),
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
    ]

    STATUS_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('VENCIDO', 'Vencido'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name='Tenant'
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name='Usuario'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Monto del Préstamo'
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Tasa de Interés (%)'
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        verbose_name='Frecuencia de Pago'
    )
    total_payments = models.PositiveIntegerField(verbose_name='Número de Pagos')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVO',
        verbose_name='Estado'
    )
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Préstamo #{self.id} - {self.user_profile.full_name} - ${self.amount}"

    @property
    def total_amount(self):
        """Calcula el monto total a pagar (capital + intereses)."""
        interest_amount = (self.amount * self.interest_rate) / 100
        return self.amount + interest_amount

    @property
    def payment_amount(self):
        """Calcula el monto del primer pago (ya que pueden ser irregulares en el caso mensual)."""
        if self.payment_frequency == 'MENSUAL':
            return self.amount * Decimal('0.80')
        return self.total_amount / self.total_payments

    @property
    def paid_amount(self):
        """Calcula el monto total pagado."""
        from apps.payments.models import Payment
        return Payment.objects.filter(loan=self, status='COMPLETADO').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

    @property
    def remaining_amount(self):
        """Calcula el monto pendiente."""
        return self.total_amount - self.paid_amount

    @property
    def completed_payments_count(self):
        """Cuenta los pagos completados."""
        from apps.payments.models import Payment
        return Payment.objects.filter(loan=self, status='COMPLETADO').count()

    @property
    def pending_payments_count(self):
        """Cuenta los pagos pendientes."""
        return self.total_payments - self.completed_payments_count