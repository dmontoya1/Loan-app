"""
URLs de reportes.
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_dashboard_view, name='dashboard'),
    path('loans/', views.loans_report_view, name='loans'),
    path('loans/export-pdf/', views.export_loans_report_pdf, name='loans_export_pdf'),
    path('payments/', views.payments_report_view, name='payments'),
    path('payments/export-pdf/', views.export_payments_report_pdf, name='payments_export_pdf'),
]
