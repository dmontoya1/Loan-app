"""
User models for loan recipients.
"""
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.authentication.models import Tenant


class Codeudor(models.Model):
    """
    Modelo para codeudores de usuarios.
    """
    DOCUMENT_TYPES = [
        ('DNI', 'DNI'),
        ('CEDULA', 'Cédula'),
        ('PASAPORTE', 'Pasaporte'),
        ('OTRO', 'Otro'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='codeudores',
        verbose_name='Tenant'
    )
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener formato: '+999999999'. Hasta 15 dígitos."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Teléfono')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='CEDULA', verbose_name='Tipo de Documento')
    document_number = models.CharField(max_length=50, unique=True, verbose_name='Número de Documento')
    address = models.TextField(verbose_name='Dirección')
    relationship = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Parentesco/Relación',
        help_text='Ej: Esposo/a, Familiar, Amigo, etc.'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Codeudor'
        verbose_name_plural = 'Codeudores'
        ordering = ['-created_at']
        unique_together = ['tenant', 'document_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.document_number})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    """
    Perfil de usuario que puede recibir préstamos.
    """
    DOCUMENT_TYPES = [
        ('DNI', 'DNI'),
        ('CEDULA', 'Cédula'),
        ('PASAPORTE', 'Pasaporte'),
        ('OTRO', 'Otro'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='user_profiles',
        verbose_name='Tenant'
    )
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener formato: '+999999999'. Hasta 15 dígitos."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Teléfono')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='CEDULA', verbose_name='Tipo de Documento')
    document_number = models.CharField(max_length=50, unique=True, verbose_name='Número de Documento')
    address = models.TextField(verbose_name='Dirección')
    codeudor = models.ForeignKey(
        'Codeudor',
        on_delete=models.SET_NULL,
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name='Codeudor'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['-created_at']
        unique_together = ['tenant', 'document_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.document_number})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
