"""
Filtros avanzados para préstamos.
"""
import django_filters
from .models import Loan
from decimal import Decimal


class LoanFilter(django_filters.FilterSet):
    """
    Filtros avanzados para préstamos.
    """
    search = django_filters.CharFilter(
        method='filter_search',
        label='Búsqueda'
    )
    
    amount_min = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        label='Monto mínimo'
    )
    
    amount_max = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        label='Monto máximo'
    )
    
    date_from = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label='Fecha desde'
    )
    
    date_to = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='lte',
        label='Fecha hasta'
    )
    
    class Meta:
        model = Loan
        fields = ['status', 'payment_frequency']
    
    def filter_search(self, queryset, name, value):
        """
        Búsqueda en múltiples campos.
        """
        if value:
            return queryset.filter(
                django_filters.Q(user_profile__first_name__icontains=value) |
                django_filters.Q(user_profile__last_name__icontains=value) |
                django_filters.Q(user_profile__document_number__icontains=value) |
                django_filters.Q(user_profile__email__icontains=value) |
                django_filters.Q(user_profile__phone__icontains=value)
            )
        return queryset
