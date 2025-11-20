"""
Formularios de préstamos.
"""
from django import forms
from .models import Loan, LoanTemplate
from apps.users.models import UserProfile


class LoanForm(forms.ModelForm):
    """
    Formulario de préstamo.
    """
    template = forms.ModelChoiceField(
        queryset=LoanTemplate.objects.none(),
        required=False,
        label='Usar Plantilla',
        help_text='Selecciona una plantilla para prellenar los campos',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
            'onchange': 'loadTemplate(this.value)'
        })
    )
    
    class Meta:
        model = Loan
        fields = ['user_profile', 'amount', 'interest_rate', 'payment_frequency', 'total_payments', 'start_date', 'notes']
        widgets = {
            'user_profile': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0.01'
            }),
            'interest_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0'
            }),
            'payment_frequency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'total_payments': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'min': '1'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        super().__init__(*args, **kwargs)
        
        if tenant:
            self.fields['user_profile'].queryset = UserProfile.objects.filter(
                tenant=tenant,
                is_active=True
            ).order_by('first_name', 'last_name')
            self.fields['user_profile'].empty_label = 'Selecciona un usuario'
            
            # Filtrar plantillas por tenant
            self.fields['template'].queryset = LoanTemplate.objects.filter(
                tenant=tenant,
                is_active=True
            ).order_by('name')
            self.fields['template'].empty_label = 'Ninguna (crear desde cero)'
            
            # Reordenar campos para mostrar template primero
            field_order = ['template', 'user_profile', 'amount', 'interest_rate', 'payment_frequency', 'total_payments', 'start_date', 'notes']
            self.fields = {field: self.fields[field] for field in field_order if field in self.fields}


class LoanImportForm(forms.ModelForm):
    """
    Formulario para importar préstamos existentes con pagos ya realizados.
    """
    payments_completed = forms.IntegerField(
        label='Cuotas Pagadas',
        required=False,
        initial=0,
        min_value=0,
        help_text='Número de cuotas que ya han sido pagadas',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
            'min': '0'
        })
    )
    
    last_payment_date = forms.DateField(
        label='Fecha del Último Pago',
        required=False,
        help_text='Fecha en que se realizó el último pago',
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
            'type': 'date'
        })
    )

    class Meta:
        model = Loan
        fields = ['user_profile', 'amount', 'interest_rate', 'payment_frequency', 'total_payments', 'start_date', 'notes']
        widgets = {
            'user_profile': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0.01'
            }),
            'interest_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0'
            }),
            'payment_frequency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'total_payments': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'min': '1'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        super().__init__(*args, **kwargs)
        
        if tenant:
            self.fields['user_profile'].queryset = UserProfile.objects.filter(
                tenant=tenant,
                is_active=True
            ).order_by('first_name', 'last_name')
            self.fields['user_profile'].empty_label = 'Selecciona un usuario'
        
        # Ordenar campos personalizados
        self.fields['payments_completed'].widget.attrs['max'] = self.fields['total_payments'].widget.attrs.get('min', 1)

    def clean(self):
        cleaned_data = super().clean()
        payments_completed = cleaned_data.get('payments_completed', 0)
        total_payments = cleaned_data.get('total_payments', 0)
        
        if payments_completed and total_payments:
            if payments_completed > total_payments:
                raise forms.ValidationError({
                    'payments_completed': f'No puedes tener más pagos completados ({payments_completed}) que el total de pagos ({total_payments}).'
                })
        
        return cleaned_data


class LoanTemplateForm(forms.ModelForm):
    """
    Formulario para crear/editar plantillas de préstamos.
    """
    class Meta:
        model = LoanTemplate
        fields = ['name', 'amount', 'interest_rate', 'payment_frequency', 'total_payments', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0.01'
            }),
            'interest_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'step': '0.01',
                'min': '0'
            }),
            'payment_frequency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all'
            }),
            'total_payments': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'min': '1'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[#22D3EE] focus:border-[#22D3EE] transition-all',
                'rows': 3
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-[#22D3EE] focus:ring-[#22D3EE] border-gray-300 rounded'
            }),
        }