"""
URLs de usuarios.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserProfileListView.as_view(), name='list'),
    path('create/', views.UserProfileCreateView.as_view(), name='create'),
    path('<int:pk>/', views.UserProfileDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UserProfileUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserProfileDeleteView.as_view(), name='delete'),
]
