"""
Admin configuration for users app.
"""
from django.contrib import admin
from .models import UserProfile, Codeudor


@admin.register(Codeudor)
class CodeudorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'document_number', 'phone', 'tenant', 'created_at']
    list_filter = ['tenant', 'document_type', 'created_at']
    search_fields = ['first_name', 'last_name', 'document_number', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Personal', {
            'fields': ('tenant', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Documentación', {
            'fields': ('document_type', 'document_number')
        }),
        ('Dirección y Relación', {
            'fields': ('address', 'relationship')
        }),
        ('Estado', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'document_number', 'phone', 'tenant', 'codeudor', 'is_active', 'created_at']
    list_filter = ['tenant', 'is_active', 'document_type', 'created_at']
    search_fields = ['first_name', 'last_name', 'document_number', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Personal', {
            'fields': ('tenant', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Documentación', {
            'fields': ('document_type', 'document_number')
        }),
        ('Dirección y Codeudor', {
            'fields': ('address', 'codeudor')
        }),
        ('Estado', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
