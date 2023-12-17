from django.contrib.auth import get_user_model, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utils.phone_number_verification import (
    generate_pre_2fa_token,
    get_user_by_token,
    send_phone_number_verification
)

from .models import CustomUser, PhoneNumberVerification, EmployeeSchedule, EmployeeWorkdays
from .permissions import IsPhoneNumberVerified, IsWaiter, IsEmployee
from .serializers import (
    AdminLoginSerializer, ClientBirthDateSerializer,
    ClientConfirmPhoneNumberSerializer,
    ClientEditProfileSerializer, CustomUserSerializer,
    LoginForClientSerializer, LoginSerializer,
    ProfileSerializer, WaiterLoginSerializer,
)

from apps.storage.serializers import EmployeeScheduleSerializer

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number"
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="First name"
            ),
            "birth_date": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Birth date in format YYYY-MM-DD. Not required",
                example="1999-01-01",
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number"
            ),
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING, description="Refresh token"
            ),
            "access": openapi.Schema(
                type=openapi.TYPE_STRING, description="Access token"
            ),
            "message": openapi.Schema(type=openapi.TYPE_STRING, description="Message"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Register user",
        operation_description="Use this method to register a user",
        request_body=manual_request_schema,
        responses={201: manual_response_schema},
    )
    def post(self, request):
        phone_number = str(request.data["phone_number"])
        first_name = request.data["first_name"]
        birth_date = request.data["birth_date"]
        data = {
            "phone_number": phone_number,
            "first_name": first_name,
            "birth_date": birth_date,
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
    serializer_class = ClientConfirmPhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "code": openapi.Schema(type=openapi.TYPE_STRING, description="Code"),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
            "response": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Response"
            ),
        },
    )

    manual_response_schema_for_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
            "response": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Response"
            ),
        },
    )

    manual_response_schema_for_404 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
            "response": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Response"
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Confirm phone number",
        operation_description="Use this method to confirm phone number",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        code = request.data["code"]
        user = CustomUser.objects.get(id=request.user.id)
        verification = PhoneNumberVerification.objects.filter(user=user, code=code)
        if verification.exists() and not verification.first().is_expired():
            user.is_verified = True
            user.save()
            return Response(
                {
                    "detail": "Поздравляем, ваш номер телефона подтвержден!",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "detail": "Код введен неверно, попробуйте еще раз",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendCodeView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [permissions.IsAuthenticated]
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Resend code",
        operation_description="Use this method to resend code",
        responses={200: manual_response_schema},
    )
    def get(self, request):
        user = request.user
        verification = send_phone_number_verification(user.id)
        return Response(
            {"detail": "Код был отправлен заново"}, status=status.HTTP_200_OK
        )


class ClientBirthDateView(generics.GenericAPIView):
    serializer_class = ClientBirthDateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "birth_date": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Birth date in format YYYY-MM-DD",
                example="1999-01-01",
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Set birth date",
        operation_description="Use this method to set birth date",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        user = request.user
        birth_date = request.data["birth_date"]
        user.birth_date = birth_date
        user.save()
        return Response(
            {"detail": "Дата рождения сохранена"}, status=status.HTTP_200_OK
        )


class ClientEditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]
    serializer_class = ClientEditProfileSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="First name of the user"
            ),
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number of the user"
            ),
            "birth_date": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Birth date in format YYYY-MM-DD",
                example="1999-01-01",
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Edit profile",
        operation_description="Use this method to edit profile",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def put(self, request):
        user = request.user
        first_name = request.data.get("first_name", user.first_name)
        phone_number = request.data.get("phone_number", user.phone_number)
        birth_date = request.data.get("birth_date", user.birth_date)
        user.first_name = first_name
        user.phone_number = phone_number
        user.birth_date = birth_date
        user.save()
        return Response(
            {"detail": "Профиль успешно изменен"}, status=status.HTTP_200_OK
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Phone number",
                example="+996777777777",
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="First name", example="John"
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "pre_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="Pre token for 2fa"
            ),
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Use this method to log the user in. The endpoint will return a temporary token to confirm two-factor authentication. To confirm, use this token in the 'Authorization' header and navigate to the following endpoint '/confirm-login/'",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        phone_number = str(request.data["phone_number"])
        first_name = request.data["first_name"]
        try:
            user = CustomUser.objects.get(
                phone_number=phone_number, first_name=first_name
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            send_phone_number_verification(user.id)
            pre_token = generate_pre_2fa_token(user)
            return Response(
                {
                    "pre_token": pre_token,
                    "detail": f"Введите 4-х значный код, отправленный на номер {user.phone_number}",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Пользователь не подтвержден"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TemporaryLoginView(generics.GenericAPIView):
    serializer_class = LoginForClientSerializer

    def post(self, request):
        phone_number = request.data["phone_number"]
        user = CustomUser.objects.get(phone_number=phone_number)
        refresh = RefreshToken.for_user(user)
        token_auth = str(refresh.access_token)
        user.token_auth = token_auth
        login(request, user)
        return Response(
            {
                "phone_number": str(user.phone_number),
                "refresh": str(refresh),
                "access": user.token_auth,
                "detail": "Вы успешно авторизованы",
            },
            status=status.HTTP_200_OK,
        )


class ClientConfirmLoginView(generics.GenericAPIView):
    serializer_class = ClientConfirmPhoneNumberSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "code": openapi.Schema(type=openapi.TYPE_STRING, description="Code"),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number"
            ),
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING, description="Refresh token"
            ),
            "access": openapi.Schema(
                type=openapi.TYPE_STRING, description="Access token"
            ),
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )
    manual_response_schema_for_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Confirm login",
        operation_description="Use this method to confirm login. The endpoint will return a refresh and access token. Use the access token in the 'Authorization' header to access protected endpoints. The refresh token can be used to get a new access token when the old one expires.",
        request_body=manual_request_schema,
        responses={200: manual_response_schema, 400: manual_response_schema_for_400},
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
                    "detail": "Вы успешно авторизованы",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Код введен неверно, попробуйте еще раз"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ClientUserProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number"
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="First name"
            ),
            "birth_date": openapi.Schema(
                type=openapi.TYPE_STRING, description="Birth date"
            ),
            "bonus": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Bonus points"
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Get user profile",
        operation_description="Use this method to get user profile. The endpoint will return user profile.",
        responses={200: manual_response_schema},
    )
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminLoginView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
    )

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING, description="Refresh token"
            ),
            "access": openapi.Schema(
                type=openapi.TYPE_STRING, description="Access token"
            ),
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )
    manual_response_schema_for_400 = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Admin login",
        operation_description="Use this method to log the admin in. The endpoint will return a refresh and access token. Use the access token in the 'Authorization' header to access protected endpoints. The refresh token can be used to get a new access token when the old one expires.",
        request_body=manual_request_schema,
        responses={
            200: manual_response_schema,
            400: manual_response_schema_for_400,
            404: manual_response_schema_for_400,
        },
    )
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.is_staff:
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                token_auth = str(refresh.access_token)
                user.token_auth = token_auth
                login(request, user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": user.token_auth,
                        "detail": "Вы успешно авторизованы",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Неверный пароль"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Пользователь не является администратором"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginForClientView(generics.GenericAPIView):
    serializer_class = LoginForClientSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Phone number",
                example="+996777777777",
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "pre_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="Pre token for 2fa"
            ),
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Login for client",
        operation_description="Use this method to log the client in. The endpoint will return a temporary token to confirm two-factor authentication. To confirm, use this token in the 'Authorization' header and navigate to the following endpoint '/confirm-login-for-client/'",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        phone_number = str(request.data["phone_number"])
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            send_phone_number_verification(user.id)
            pre_token = generate_pre_2fa_token(user)
            return Response(
                {
                    "pre_token": pre_token,
                    "detail": f"Введите 4-х значный код, отправленный на номер {user.phone_number}",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Пользователь не подтвержде"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class WaiterLoginView(generics.GenericAPIView):
    serializer_class = WaiterLoginSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Login",
                example="Hasbik",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="password", example="Has6ig007"
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "pre_token": openapi.Schema(
                type=openapi.TYPE_STRING, description="Pre token for 2fa"
            ),
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Use this method to log the user in. The endpoint will return a temporary token to confirm two-factor authentication. To confirm, use this token in the 'Authorization' header and navigate to the following endpoint '/confirm-login/'",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                token_auth = str(refresh.access_token)
                user.token_auth = token_auth
                login(request, user)
                if user.is_verified:
                    send_phone_number_verification(user.id)
                    pre_token = generate_pre_2fa_token(user)
                    return Response(
                        {
                            "pre_token": pre_token,
                            "detail": f"Введите 4-х значный код, отправленный на номер {user.username}",
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "Пользователь не подтвержден"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )


class WaiterTemporaryLoginView(generics.GenericAPIView):
    serializer_class = WaiterLoginSerializer
    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Login",
                example="Hasbik",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="password", example="Has6ig007"
            ),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING, description="Refresh token"
            ),
            "access": openapi.Schema(
                type=openapi.TYPE_STRING, description="Access token"
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Use this method to log the user in. The endpoint will return a temporary token to confirm two-factor authentication. To confirm, use this token in the 'Authorization' header and navigate to the following endpoint '/confirm-login/'",
        request_body=manual_request_schema,
        responses={200: manual_response_schema},
    )
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                token_auth = str(refresh.access_token)
                user.token_auth = token_auth
                login(request, user)
                return Response(
                    {
                        "phone_number": str(user.phone_number),
                        "refresh": str(refresh),
                        "access": user.token_auth,
                        "detail": "Вы успешно авторизованы",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )


class ResendCodeWithPreTokenView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Detail"),
        },
    )

    @swagger_auto_schema(
        operation_summary="Resend code",
        operation_description="Use this method to resend code",
        responses={200: manual_response_schema},
    )
    def get(self, request):
        user = request.user
        pre_token = request.headers.get("Authorization")
        user = get_user_by_token(pre_token)
        send_phone_number_verification(user.id)
        return Response(
            {"detail": "Код был отправлен заново"}, status=status.HTTP_200_OK
        )


class EmployeeScheduleView(generics.GenericAPIView):
    serializer_class = EmployeeScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def get(self, request):
        user = request.user
        schedule = EmployeeSchedule.objects.filter(employees=user)
        serializer = EmployeeScheduleSerializer(schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)