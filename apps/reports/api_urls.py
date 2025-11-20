"""
API URLs para reportes.
"""
from django.urls import path
from . import api_views

app_name = 'api_reports'

urlpatterns = [
    path('dashboard/', api_views.dashboard_stats, name='dashboard'),
    path('loans/', api_views.loans_report, name='loans_report'),
    path('payments/', api_views.payments_report, name='payments_report'),
]

