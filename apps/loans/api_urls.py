"""
API URLs para préstamos.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'loans', api_views.LoanViewSet, basename='loan')
router.register(r'templates', api_views.LoanTemplateViewSet, basename='loantemplate')

app_name = 'api_loans'

urlpatterns = [
    path('', include(router.urls)),
]

