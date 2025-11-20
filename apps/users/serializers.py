"""
Serializers para usuarios.
"""
from rest_framework import serializers
from .models import UserProfile, Codeudor


class CodeudorSerializer(serializers.ModelSerializer):
    """Serializer para Codeudor."""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Codeudor
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'document_type', 'document_number', 'address', 'relationship',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para UserProfile."""
    full_name = serializers.CharField(read_only=True)
    codeudor_detail = CodeudorSerializer(source='codeudor', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'document_type', 'document_number', 'address', 'codeudor',
                  'codeudor_detail', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de usuarios."""
    full_name = serializers.CharField(read_only=True)
    loans_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'email', 'phone', 'document_number',
                  'is_active', 'loans_count', 'created_at']
    
    def get_loans_count(self, obj):
        return obj.loans.count()

