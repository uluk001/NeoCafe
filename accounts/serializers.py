from rest_framework import serializers
from .models import CustomUser
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator

class CustomUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[
            RegexValidator(regex=r'^\+996\d{9}$', message='Номер должен быть в формате +996XXXXXXXXX', code='invalid_phone'),
            UniqueValidator(queryset=CustomUser.objects.all(), message='Этот номер телефона уже зарегистрирован.')
        ]
    )
    name = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True)
    verification_code = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('phone', 'name', 'birth_date', 'verification_code')

    def create(self, validated_data):
        validated_data['verification_code'] = get_random_string(length=4, allowed_chars='0123456789')
        user = CustomUser.objects.create(**validated_data)
        # Логика отправки SMS через Infobip должна быть здесь
        return user

    # Метод для отправки SMS через Infobip будет здесь
    def send_verification_code_sms(self, phone, code):
        # Ваш код для интеграции с Infobip
        pass
