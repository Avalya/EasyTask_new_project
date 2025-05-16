from rest_framework import serializers
from .models import Application

# 🔹 Сериализатор заявок
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'  
        read_only_fields = ['reg_number', 'submitted_at']


# 🔹 Кастомный токен сериализатор для добавления роли
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 👇 Добавляем роль в токен
        if user.is_superuser:
            token['role'] = 'admin'
        else:
            token['role'] = 'department'

        return token

