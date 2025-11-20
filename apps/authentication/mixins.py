"""
Mixins para vistas (DRY principle).
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class TenantRequiredMixin(LoginRequiredMixin):
    """
    Mixin que requiere que el usuario tenga un tenant.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not hasattr(request.user, 'tenant') or not request.user.tenant:
            raise PermissionDenied("No tienes un tenant asignado.")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filtra el queryset por tenant del usuario.
        """
        queryset = super().get_queryset()
        if hasattr(queryset.model, 'tenant'):
            return queryset.filter(tenant=self.request.user.tenant)
        return queryset
