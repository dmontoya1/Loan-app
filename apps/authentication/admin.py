"""
Admin configuration for authentication app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Tenant

CustomUser = get_user_model()


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'tenant', 'is_tenant_admin', 'is_staff']
    list_filter = ['tenant', 'is_tenant_admin', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('tenant', 'phone', 'is_tenant_admin')}),
    )
