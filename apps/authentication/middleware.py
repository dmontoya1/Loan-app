"""
Middleware para manejar multi-tenancy.
"""
from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware que establece el tenant actual en el request.
    """
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'tenant'):
            request.tenant = request.user.tenant
        else:
            request.tenant = None
        return None
