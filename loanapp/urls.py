"""
URL configuration for loanapp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Web URLs
    path('', include('apps.authentication.urls')),
    path('prestamos/', include('apps.loans.urls')),
    path('usuarios/', include('apps.users.urls')),
    path('pagos/', include('apps.payments.urls')),
    path('reportes/', include('apps.reports.urls')),
    # API URLs
    path('api/auth/', include('apps.authentication.api_urls')),
    path('api/users/', include('apps.users.api_urls')),
    path('api/loans/', include('apps.loans.api_urls')),
    path('api/payments/', include('apps.payments.api_urls')),
    path('api/reports/', include('apps.reports.api_urls')),
    # JWT Token URLs
    path('api/token/', include('rest_framework_simplejwt.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
