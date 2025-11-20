"""
API URLs para usuarios.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'profiles', api_views.UserProfileViewSet, basename='userprofile')
router.register(r'codeudores', api_views.CodeudorViewSet, basename='codeudor')

app_name = 'api_users'

urlpatterns = [
    path('', include(router.urls)),
]

