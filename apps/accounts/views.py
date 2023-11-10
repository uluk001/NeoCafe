from django.contrib.auth import get_user_model, login
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utils.phone_number_verification import send_phone_number_verification, generate_pre_2fa_token, get_user_by_token

from .models import CustomUser, PhoneNumberVerification
from .serializers import ClientConfirmPhoneNumberSerializer, CustomUserSerializer, ClientBirthDateSerializer, ClientEditProfileSerializer, LoginSerializer
from .permissions import IsPhoneNumberVerified
from drf_yasg.utils import swagger_auto_schema


User = get_user_model()


class RegisterView(generics.GenericAPIView):
    """
    Register user.

    Use this endpoint to register new user.

    Parameters:
    - `phone_number`: Phone number of the user
    - `first_name`: First name of the user
    """
    
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={201: CustomUserSerializer}
    )

    def post(self, request):
        phone_number = str(request.data["phone_number"])
        first_name = request.data["first_name"]
        data = {
            "phone_number": phone_number,
            "first_name": first_name,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        verification = send_phone_number_verification(user.id)
        token_auth = str(refresh.access_token)
        user.token_auth = token_auth


        response_data = {
            "phone_number": str(user.phone_number),
            "refresh": str(refresh),
            "access": user.token_auth,
            "message": f"Введите 4-х значный код, отправленный на номер {user.phone_number}",
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class ClientConfirmPhoneNumberView(generics.GenericAPIView):
    """
    Confirm phone number.

    Use this endpoint to confirm user phone number.

    Parameters:
    - `code`: Code for phone number confirmation
    """

    serializer_class = ClientConfirmPhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data["code"]
        user = CustomUser.objects.get(id=request.user.id)
        verification = PhoneNumberVerification.objects.filter(user=user, code=code)
        response = 0
        if verification.exists() and not verification.first().is_expired():
            user.is_verified = True
            user.save()
            response = 1
            return Response(
                {
                    "detail": "Поздравляем, ваш номер телефона подтвержден!",
                    "response": response
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "detail": "Код введен неверно, попробуйте еще раз",
                    "response": response
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ResendCodeView(generics.GenericAPIView):
    """
    Resend code.

    Use this endpoint to resend code.

    Parameters:
    - `phone_number`: Phone number of the user
    """

    serializer_class = serializers.Serializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: serializers.Serializer}
    )

    def post(self, request):
        user = request.user
        verification = send_phone_number_verification(user.id)
        return Response({"detail": "Код был отправлен заново"}, status=status.HTTP_200_OK)


class ClientBirthDateView(generics.GenericAPIView):
    """
    Birth date.

    Use this endpoint to set birth date.

    Parameters:
    - `birth_date`: Birth date of the user
    """

    serializer_class = ClientBirthDateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]
    
    @swagger_auto_schema(
        request_body=ClientBirthDateSerializer,
        responses={200: ClientBirthDateSerializer}
    )

    def post(self, request):
        user = request.user
        birth_date = request.data["birth_date"]
        user.birth_date = birth_date
        user.save()
        return Response({"detail": "Дата рождения сохранена"}, status=status.HTTP_200_OK)


class ClientEditProfileView(APIView):
    """
    Edit profile.

    Use this endpoint to edit user profile.

    Parameters:
    - `first_name`: First name of the user
    - `phone_number`: Phone number of the user
    - `birth_date`: Birth date of the user
    """
    
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]
    serializer_class = ClientEditProfileSerializer

    @swagger_auto_schema(
        request_body=ClientEditProfileSerializer,
        responses={200: ClientEditProfileSerializer}
    )
    
    def post(self, request):
        user = request.user
        first_name = request.data["first_name"]
        phone_number = request.data["phone_number"]
        birth_date = request.data["birth_date"]
        user.first_name = first_name
        user.phone_number = phone_number
        user.birth_date = birth_date
        user.save()
        return Response({"detail": "Профиль успешно изменен"}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    """
    Login user.

    Use this endpoint to login user.

    Parameters:
    - `phone_number`: Phone number of the user
    """

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: LoginSerializer}
    )

    def post(self, request):
        phone_number = str(request.data["phone_number"])
        first_name = request.data["first_name"]
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            send_phone_number_verification(user.id)
            pre_token = generate_pre_2fa_token(user)
            return Response(
                {
                    "pre_token": pre_token,
                    "detail": f"Введите 4-х значный код, отправленный на номер {user.phone_number}"
                },
                    status=status.HTTP_200_OK
                )
        else:
            return Response({"detail": "Пользователь не подтвержден"}, status=status.HTTP_400_BAD_REQUEST)


class ClientConfirmLoginView(generics.GenericAPIView):
    """
    Confirm login.

    Use this endpoint to confirm login.

    Parameters:
    - `code`: Code for login confirmation
    """

    serializer_class = ClientConfirmPhoneNumberSerializer

    @swagger_auto_schema(
        request_body=ClientConfirmPhoneNumberSerializer,
        responses={200: ClientConfirmPhoneNumberSerializer}
    )

    def post(self, request):
        code = request.data["code"]
        pre_token = request.headers.get("Authorization")
        user = get_user_by_token(pre_token)
        verification = PhoneNumberVerification.objects.filter(user=user, code=code)
        if verification.exists() and not verification.first().is_expired():
            user.is_verified = True
            user.save()
            refresh = RefreshToken.for_user(user)
            token_auth = str(refresh.access_token)
            user.token_auth = token_auth
            login(request, user)
            return Response(
                {
                    "phone_number": str(user.phone_number),
                    "refresh": str(refresh),
                    "access": user.token_auth,
                    "detail": "Вы успешно авторизованы"
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "detail": "Код введен неверно, попробуйте еще раз"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ClientUserProfileView(generics.GenericAPIView):
    """
    User profile.

    Use this endpoint to get user profile.
    """

    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]


    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
