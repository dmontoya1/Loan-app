"""
API URLs para autenticación.
"""
from django.urls import path
from . import api_views

app_name = 'api_auth'

urlpatterns = [
    path('login/', api_views.login_view, name='login'),
    path('register/', api_views.register_view, name='register'),
    path('me/', api_views.current_user_view, name='current_user'),
]

