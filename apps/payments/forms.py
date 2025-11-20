"""
Formularios de pagos.
"""
from django import forms
from django.utils import timezone
from .models import Payment


class PaymentForm(forms.ModelForm):
    """
    Formulario de pago.
    """
    class Meta:
        model = Payment
        fields = ['status', 'payment_date', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'payment_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha actual por defecto si es un nuevo pago o no tiene fecha
        if not self.instance.payment_date:
            self.initial['payment_date'] = timezone.now().date()
