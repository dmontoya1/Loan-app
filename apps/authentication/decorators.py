"""
Decoradores para autenticación y permisos.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def tenant_required(view_func):
    """
    Decorador que verifica que el usuario tenga un tenant asignado.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        
        if not hasattr(request.user, 'tenant') or not request.user.tenant:
            messages.error(request, 'No tienes un tenant asignado.')
            return redirect('authentication:login')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
