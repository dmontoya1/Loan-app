"""
API Views para pagos.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime
from .models import Payment
from .serializers import PaymentSerializer, PaymentProcessSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para pagos."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'loan']
    search_fields = ['loan__user_profile__first_name', 'loan__user_profile__last_name',
                     'loan__user_profile__document_number']
    ordering_fields = ['due_date', 'payment_date', 'payment_number', 'created_at']
    ordering = ['due_date', 'payment_number']
    
    def get_queryset(self):
        """Filtrar por tenant."""
        queryset = super().get_queryset()
        if self.request.user.tenant:
            queryset = queryset.filter(loan__tenant=self.request.user.tenant)
        
        # Filtros adicionales
        overdue = self.request.query_params.get('overdue', 'false')
        if overdue == 'true':
            queryset = queryset.filter(
                status='VENCIDO',
                due_date__lt=timezone.now().date()
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Procesar un pago (marcarlo como completado)."""
        payment = self.get_object()
        serializer = PaymentProcessSerializer(
            data=request.data,
            context={'payment': payment}
        )
        
        if serializer.is_valid():
            payment_date = serializer.validated_data.get('payment_date')
            notes = serializer.validated_data.get('notes', '')
            
            payment.mark_as_completed(payment_date)
            if notes:
                payment.notes = notes
                payment.save()
            
            return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Obtener pagos vencidos."""
        overdue_payments = self.get_queryset().filter(
            status='VENCIDO',
            due_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(overdue_payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Obtener pagos próximos a vencer."""
        from datetime import timedelta
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        
        upcoming_payments = self.get_queryset().filter(
            status='PENDIENTE',
            due_date__gte=today,
            due_date__lte=next_week
        )
        serializer = self.get_serializer(upcoming_payments, many=True)
        return Response(serializer.data)

