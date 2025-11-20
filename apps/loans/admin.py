"""
Admin para préstamos.
"""
from django.contrib import admin
from .models import Loan, LoanTemplate


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_profile', 'amount', 'interest_rate', 'payment_frequency', 'status', 'created_at')
    list_filter = ('status', 'payment_frequency', 'created_at')
    search_fields = ('user_profile__first_name', 'user_profile__last_name', 'user_profile__document_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LoanTemplate)
class LoanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest_rate', 'payment_frequency', 'total_payments', 'is_active', 'created_at')
    list_filter = ('is_active', 'payment_frequency', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')