"""
Admin configuration for payments app.
"""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'payment_number', 'amount', 'due_date', 'payment_date', 'status']
    list_filter = ['status', 'due_date', 'created_at']
    search_fields = ['loan__user_profile__first_name', 'loan__user_profile__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información del Pago', {
            'fields': ('loan', 'payment_number', 'amount', 'due_date', 'payment_date', 'status')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
