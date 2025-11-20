"""
URLs de pagos.
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('<int:pk>/update/', views.PaymentUpdateView.as_view(), name='update'),
    path('<int:payment_id>/create/', views.create_payment_view, name='create'),
    path('<int:payment_id>/process/', views.process_payment_view, name='process'),
    path('overdue/', views.overdue_payments_view, name='overdue'),
    path('export-pdf/', views.export_payments_pdf, name='export_pdf'),
    path('export-excel/', views.export_payments_excel, name='export_excel'),
    path('<int:payment_id>/receipt/', views.export_payment_receipt_pdf, name='receipt'),
]
