"""
Formularios de usuarios.
"""
from django import forms
from .models import UserProfile, Codeudor


class CodeudorForm(forms.ModelForm):
    """
    Formulario para crear/editar codeudor.
    """
    class Meta:
        model = Codeudor
        fields = ['first_name', 'last_name', 'email', 'phone', 'document_type', 'document_number', 'address', 'relationship']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'document_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3
            }),
            'relationship': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ej: Esposo/a, Familiar, Amigo'
            }),
        }


class UserProfileForm(forms.ModelForm):
    """
    Formulario de perfil de usuario.
    """
    create_codeudor = forms.BooleanField(
        required=False,
        initial=False,
        label='Crear nuevo codeudor',
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-[#22D3EE] focus:ring-[#22D3EE] border-gray-300 rounded',
            'onchange': 'toggleCodeudorForm()'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone', 'document_type', 'document_number', 'address', 'codeudor', 'create_codeudor']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'document_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'rows': 3
            }),
            'codeudor': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
        }

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        super().__init__(*args, **kwargs)
        
        if tenant:
            self.fields['codeudor'].queryset = Codeudor.objects.filter(
                tenant=tenant
            ).order_by('first_name', 'last_name')
            self.fields['codeudor'].required = False