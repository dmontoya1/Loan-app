"""
Serializers para autenticación.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Tenant


class TenantSerializer(serializers.ModelSerializer):
    """Serializer para Tenant."""
    
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'email', 'phone', 'address', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuarios."""
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'tenant', 'tenant_name', 'is_tenant_admin', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class LoginSerializer(serializers.Serializer):
    """Serializer para login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo.')
            data['user'] = user
        else:
            raise serializers.ValidationError('Debe incluir username y password.')
        
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de tenant."""
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Tenant
        fields = ['name', 'email', 'phone', 'address', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        tenant = Tenant.objects.create(**validated_data)
        
        # Crear usuario admin para el tenant
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            tenant=tenant,
            is_tenant_admin=True,
            password=password
        )
        
        return tenant

