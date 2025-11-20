"""
API URLs para pagos.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'payments', api_views.PaymentViewSet, basename='payment')

app_name = 'api_payments'

urlpatterns = [
    path('', include(router.urls)),
]

