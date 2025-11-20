"""
API Views para autenticación.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, TenantSerializer
from .models import Tenant

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Endpoint para login."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Endpoint para registro de tenant."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        tenant = serializer.save()
        user = User.objects.get(tenant=tenant, is_tenant_admin=True)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'tenant': TenantSerializer(tenant).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user_view(request):
    """Endpoint para obtener el usuario actual."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

