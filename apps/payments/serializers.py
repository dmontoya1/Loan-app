"""
Serializers para pagos.
"""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para pagos."""
    loan_amount = serializers.DecimalField(source='loan.amount', max_digits=12, decimal_places=2, read_only=True)
    loan_user_name = serializers.CharField(source='loan.user_profile.full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'loan', 'loan_amount', 'loan_user_name', 'amount', 'due_date',
                  'payment_date', 'status', 'payment_number', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentProcessSerializer(serializers.Serializer):
    """Serializer para procesar un pago."""
    payment_date = serializers.DateField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        payment = self.context.get('payment')
        if not payment:
            raise serializers.ValidationError('Pago no encontrado.')
        if payment.status == 'COMPLETADO':
            raise serializers.ValidationError('Este pago ya fue completado.')
        return data

