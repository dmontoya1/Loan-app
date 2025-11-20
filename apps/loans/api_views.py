"""
API Views para préstamos.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Loan, LoanTemplate
from .serializers import (
    LoanListSerializer, LoanDetailSerializer, LoanCreateSerializer,
    LoanTemplateSerializer
)
from .services import PaymentFactory


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet para préstamos."""
    queryset = Loan.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_frequency']
    search_fields = [
        'user_profile__first_name', 'user_profile__last_name',
        'user_profile__document_number', 'user_profile__email',
        'user_profile__phone'
    ]
    ordering_fields = ['created_at', 'amount', 'start_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar por tenant y aplicar filtros avanzados."""
        queryset = super().get_queryset()
        
        # Filtrar por tenant
        if self.request.user.tenant:
            queryset = queryset.filter(tenant=self.request.user.tenant)
        
        # Filtros avanzados
        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def get_serializer_class(self):
        """Usar serializer diferente según la acción."""
        if self.action == 'list':
            return LoanListSerializer
        elif self.action == 'create':
            return LoanCreateSerializer
        return LoanDetailSerializer
    
    def perform_create(self, serializer):
        """Asignar tenant automáticamente."""
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=True, methods=['post'])
    def import_loan(self, request, pk=None):
        """Importar préstamo con pagos ya completados."""
        loan = self.get_object()
        payments_completed = request.data.get('payments_completed', 0)
        last_payment_date = request.data.get('last_payment_date')
        
        # Recrear pagos con los completados
        loan.payments.all().delete()
        PaymentFactory.create_payments_for_loan(
            loan,
            payments_completed=payments_completed,
            last_payment_date=last_payment_date
        )
        
        serializer = self.get_serializer(loan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Obtener pagos de un préstamo."""
        loan = self.get_object()
        from apps.payments.serializers import PaymentSerializer
        serializer = PaymentSerializer(loan.payments.all(), many=True)
        return Response(serializer.data)


class LoanTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet para plantillas de préstamos."""
    queryset = LoanTemplate.objects.all()
    serializer_class = LoanTemplateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'notes']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar por tenant."""
        queryset = super().get_queryset()
        if self.request.user.tenant:
            queryset = queryset.filter(tenant=self.request.user.tenant)
        return queryset
    
    def perform_create(self, serializer):
        """Asignar tenant automáticamente."""
        serializer.save(tenant=self.request.user.tenant)

