from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Application


# 🔹 Application Serializer
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['reg_number', 'submitted_at']


# 🔹 Custom JWT Token Serializer with Role
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['groups'] = list(user.groups.values_list('name', flat=True))

        # Add role to token
        token['role'] = 'admin' if user.is_superuser else 'department'

        return token