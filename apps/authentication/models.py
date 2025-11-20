"""
Authentication models for multi-tenancy support.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Tenant(models.Model):
    """
    Modelo para empresas/usuarios que gestionan préstamos (multi-tenancy).
    """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener formato: '+999999999'. Hasta 15 dígitos."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Teléfono')
    address = models.TextField(blank=True, verbose_name='Dirección')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Usuario extendido con soporte multi-tenant.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True,
        verbose_name='Tenant'
    )
    phone = models.CharField(max_length=17, blank=True, verbose_name='Teléfono')
    is_tenant_admin = models.BooleanField(default=False, verbose_name='Administrador del Tenant')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
        # Agregar related_name único para evitar conflictos
        permissions = [
            ("can_manage_loans", "Can manage loans"),
            ("can_manage_users", "Can manage users"),
        ]

    def __str__(self):
        return f"{self.username} ({self.tenant.name if self.tenant else 'Sin tenant'})"
