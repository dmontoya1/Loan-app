"""
Vistas de usuarios.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import UserProfile, Codeudor
from .forms import UserProfileForm, CodeudorForm
from apps.authentication.mixins import TenantRequiredMixin


class UserProfileListView(TenantRequiredMixin, ListView):
    """
    Lista de perfiles de usuario.
    """
    model = UserProfile
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(document_number__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class UserProfileCreateView(TenantRequiredMixin, CreateView):
    """
    Crear nuevo perfil de usuario.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        
        # Si se solicita crear un nuevo codeudor
        if form.cleaned_data.get('create_codeudor'):
            # Crear codeudor desde los datos del POST
            codeudor_data = {
                'first_name': self.request.POST.get('codeudor_first_name', ''),
                'last_name': self.request.POST.get('codeudor_last_name', ''),
                'email': self.request.POST.get('codeudor_email', ''),
                'phone': self.request.POST.get('codeudor_phone', ''),
                'document_type': self.request.POST.get('codeudor_document_type', 'CEDULA'),
                'document_number': self.request.POST.get('codeudor_document_number', ''),
                'address': self.request.POST.get('codeudor_address', ''),
                'relationship': self.request.POST.get('codeudor_relationship', ''),
            }
            
            codeudor_form = CodeudorForm(codeudor_data)
            if codeudor_form.is_valid():
                codeudor = codeudor_form.save(commit=False)
                codeudor.tenant = self.request.user.tenant
                codeudor.save()
                form.instance.codeudor = codeudor
            else:
                messages.error(self.request, 'Error al crear el codeudor. Por favor verifica los datos.')
                return self.form_invalid(form)
        
        messages.success(self.request, f'Usuario {form.instance.full_name} creado exitosamente.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.user.tenant
        return kwargs


class UserProfileDetailView(TenantRequiredMixin, DetailView):
    """
    Detalle de perfil de usuario.
    """
    model = UserProfile
    template_name = 'users/user_detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = self.object.loans.all().order_by('-created_at')
        return context


class UserProfileUpdateView(TenantRequiredMixin, UpdateView):
    """
    Actualizar perfil de usuario.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        # Si se solicita crear un nuevo codeudor
        if form.cleaned_data.get('create_codeudor'):
            # Crear codeudor desde los datos del POST
            codeudor_data = {
                'first_name': self.request.POST.get('codeudor_first_name', ''),
                'last_name': self.request.POST.get('codeudor_last_name', ''),
                'email': self.request.POST.get('codeudor_email', ''),
                'phone': self.request.POST.get('codeudor_phone', ''),
                'document_type': self.request.POST.get('codeudor_document_type', 'CEDULA'),
                'document_number': self.request.POST.get('codeudor_document_number', ''),
                'address': self.request.POST.get('codeudor_address', ''),
                'relationship': self.request.POST.get('codeudor_relationship', ''),
            }
            
            codeudor_form = CodeudorForm(codeudor_data)
            if codeudor_form.is_valid():
                codeudor = codeudor_form.save(commit=False)
                codeudor.tenant = self.request.user.tenant
                codeudor.save()
                form.instance.codeudor = codeudor
            else:
                messages.error(self.request, 'Error al crear el codeudor. Por favor verifica los datos.')
                return self.form_invalid(form)
        
        messages.success(self.request, f'Usuario {form.instance.full_name} actualizado exitosamente.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.user.tenant
        return kwargs


class UserProfileDeleteView(TenantRequiredMixin, DeleteView):
    """
    Eliminar perfil de usuario.
    """
    model = UserProfile
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Usuario eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
