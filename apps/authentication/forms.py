"""
Formularios de autenticación.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Tenant

CustomUser = get_user_model()


class LoginForm(forms.Form):
    """
    Formulario de login.
    """
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
            'placeholder': 'Contraseña'
        })
    )


class TenantRegistrationForm(forms.ModelForm):
    """
    Formulario de registro de tenant.
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
        })
    )
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
        })
    )

    class Meta:
        model = Tenant
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'rows': 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        tenant = super().save(commit=commit)
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        # Crear usuario asociado
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            tenant=tenant,
            is_tenant_admin=True,
        )

        return tenant


class UserRegistrationForm(UserCreationForm):
    """
    Formulario de registro de usuario del sistema.
    """
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.filter(is_active=True),
        label='Empresa',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'tenant', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
        }
