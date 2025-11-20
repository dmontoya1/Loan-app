"""
Payment models.
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.loans.models import Loan


class Payment(models.Model):
    """
    Modelo de pago.
    """
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('VENCIDO', 'Vencido'),
        ('CANCELADO', 'Cancelado'),
    ]

    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Préstamo'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Monto'
    )
    due_date = models.DateField(verbose_name='Fecha de Vencimiento')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Fecha de Pago')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDIENTE',
        verbose_name='Estado'
    )
    payment_number = models.PositiveIntegerField(verbose_name='Número de Pago')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['payment_number', 'due_date']
        unique_together = ['loan', 'payment_number']

    def __str__(self):
        return f"Pago #{self.payment_number} - {self.loan} - ${self.amount} ({self.status})"

    def mark_as_completed(self, payment_date=None):
        """Marca el pago como completado."""
        self.status = 'COMPLETADO'
        if payment_date:
            self.payment_date = payment_date
        else:
            from django.utils import timezone
            self.payment_date = timezone.now().date()
        self.save()
