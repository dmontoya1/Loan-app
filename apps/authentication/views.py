"""
Vistas de autenticación.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Tenant
from .forms import TenantRegistrationForm, UserRegistrationForm, LoginForm

CustomUser = get_user_model()


def login_view(request):
    """
    Vista de login.
    """
    if request.user.is_authenticated:
        return redirect('loans:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.username}!')
                return redirect('loans:dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


class TenantRegistrationView(CreateView):
    """
    Vista de registro de tenant (empresa).
    """
    model = Tenant
    form_class = TenantRegistrationForm
    template_name = 'authentication/register_tenant.html'
    success_url = reverse_lazy('authentication:login')

    def form_valid(self, form):
        messages.success(self.request, 'Tenant registrado exitosamente. Ahora puedes iniciar sesión.')
        return super().form_valid(form)


class UserRegistrationView(CreateView):
    """
    Vista de registro de usuario del sistema.
    """
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'authentication/register_user.html'
    success_url = reverse_lazy('authentication:login')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return super().form_valid(form)


@login_required
def logout_view(request):
    """
    Vista de logout.
    """
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('authentication:login')
