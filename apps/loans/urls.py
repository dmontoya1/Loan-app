"""
URLs de préstamos.
"""
from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('list/', views.LoanListView.as_view(), name='list'),
    path('create/', views.LoanCreateView.as_view(), name='create'),
    path('import/', views.LoanImportView.as_view(), name='import'),
    path('export-pdf/', views.export_loans_pdf, name='export_pdf'),
    path('export-excel/', views.export_loans_excel, name='export_excel'),
    path('templates/', views.LoanTemplateListView.as_view(), name='templates'),
    path('templates/create/', views.LoanTemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/update/', views.LoanTemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:pk>/delete/', views.LoanTemplateDeleteView.as_view(), name='template_delete'),
    path('api/templates/<int:template_id>/', views.get_template_json, name='template_json'),
    path('<int:pk>/', views.LoanDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.LoanUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LoanDeleteView.as_view(), name='delete'),
]