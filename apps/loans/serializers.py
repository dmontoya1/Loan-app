"""
Serializers para préstamos.
"""
from rest_framework import serializers
from .models import Loan, LoanTemplate
from apps.users.serializers import UserProfileSerializer


class LoanTemplateSerializer(serializers.ModelSerializer):
    """Serializer para plantillas de préstamos."""
    
    class Meta:
        model = LoanTemplate
        fields = ['id', 'name', 'amount', 'interest_rate', 'payment_frequency',
                  'total_payments', 'notes', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoanListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de préstamos."""
    user_profile_name = serializers.CharField(source='user_profile.full_name', read_only=True)
    user_profile_document = serializers.CharField(source='user_profile.document_number', read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    paid_amount = serializers.SerializerMethodField()
    pending_amount = serializers.SerializerMethodField()
    completed_payments = serializers.SerializerMethodField()
    total_payments_count = serializers.IntegerField(source='total_payments', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'user_profile_name', 'user_profile_document', 'amount',
                  'interest_rate', 'payment_frequency', 'total_payments_count',
                  'start_date', 'status', 'total_amount', 'paid_amount',
                  'pending_amount', 'completed_payments', 'created_at']
    
    def get_paid_amount(self, obj):
        return obj.paid_amount
    
    def get_pending_amount(self, obj):
        return obj.pending_amount
    
    def get_completed_payments(self, obj):
        return obj.payments.filter(status='COMPLETADO').count()


class LoanDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle de préstamo."""
    user_profile = UserProfileSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    paid_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    pending_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    completed_payments = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        fields = ['id', 'user_profile', 'amount', 'interest_rate', 'payment_frequency',
                  'total_payments', 'start_date', 'status', 'notes', 'total_amount',
                  'paid_amount', 'pending_amount', 'completed_payments', 'payments',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_completed_payments(self, obj):
        return obj.payments.filter(status='COMPLETADO').count()
    
    def get_payments(self, obj):
        from apps.payments.serializers import PaymentSerializer
        return PaymentSerializer(obj.payments.all(), many=True).data


class LoanCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear préstamos."""
    
    class Meta:
        model = Loan
        fields = ['user_profile', 'amount', 'interest_rate', 'payment_frequency',
                  'total_payments', 'start_date', 'status', 'notes', 'template']
        extra_kwargs = {
            'status': {'required': False},
            'template': {'required': False, 'write_only': True}
        }
    
    def create(self, validated_data):
        template = validated_data.pop('template', None)
        
        # Si hay template, aplicar valores
        if template:
            if 'amount' not in validated_data or not validated_data['amount']:
                validated_data['amount'] = template.amount
            if 'interest_rate' not in validated_data or not validated_data['interest_rate']:
                validated_data['interest_rate'] = template.interest_rate
            if 'payment_frequency' not in validated_data or not validated_data['payment_frequency']:
                validated_data['payment_frequency'] = template.payment_frequency
            if 'total_payments' not in validated_data or not validated_data['total_payments']:
                validated_data['total_payments'] = template.total_payments
        
        # Obtener tenant del request
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.tenant:
            validated_data['tenant'] = request.user.tenant
        
        loan = Loan.objects.create(**validated_data)
        
        # Crear pagos automáticamente
        from .services import PaymentFactory
        PaymentFactory.create_payments_for_loan(loan)
        
        return loan

