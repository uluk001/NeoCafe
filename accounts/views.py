from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from .models import CustomUser
import requests
from django.conf import settings

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Отправляем SMS через Infobip
            send_sms(user.phone, user.verification_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Функция для отправки SMS через Infobip
def send_sms(phone, code):
    # Реализация отправки SMS через Infobip
    pass

# Добавим представление для авторизации
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            user = CustomUser.objects.get(phone=phone)
            if user:
                # Проверка и отправка кода подтверждения
                user.set_verification_code()
                send_sms(user.phone, user.verification_code)
                return Response({'message': 'Код подтверждения отправлен.'}, status=status.HTTP_200_OK)
            return Response({'message': 'Пользователь с таким номером не найден.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
