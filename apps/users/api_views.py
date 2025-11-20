"""
API Views para usuarios.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile, Codeudor
from .serializers import UserProfileSerializer, UserProfileListSerializer, CodeudorSerializer
from apps.authentication.mixins import TenantRequiredMixin


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para UserProfile."""
    queryset = UserProfile.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'document_number', 'phone']
    ordering_fields = ['created_at', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar por tenant."""
        queryset = super().get_queryset()
        if self.request.user.tenant:
            queryset = queryset.filter(tenant=self.request.user.tenant)
        return queryset
    
    def get_serializer_class(self):
        """Usar serializer diferente para listado."""
        if self.action == 'list':
            return UserProfileListSerializer
        return UserProfileSerializer
    
    def perform_create(self, serializer):
        """Asignar tenant automáticamente."""
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=True, methods=['get'])
    def loans(self, request, pk=None):
        """Obtener préstamos de un usuario."""
        user_profile = self.get_object()
        from apps.loans.serializers import LoanListSerializer
        loans = user_profile.loans.all()
        serializer = LoanListSerializer(loans, many=True)
        return Response(serializer.data)


class CodeudorViewSet(viewsets.ModelViewSet):
    """ViewSet para Codeudor."""
    queryset = Codeudor.objects.all()
    serializer_class = CodeudorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'document_number', 'email', 'phone']
    
    def get_queryset(self):
        """Filtrar por tenant."""
        queryset = super().get_queryset()
        if self.request.user.tenant:
            queryset = queryset.filter(tenant=self.request.user.tenant)
        return queryset
    
    def perform_create(self, serializer):
        """Asignar tenant automáticamente."""
        serializer.save(tenant=self.request.user.tenant)

