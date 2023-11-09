# from django.contrib.auth import get_user_model, login
# from django.shortcuts import redirect
# from rest_framework import generics, permissions, serializers, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken

# from utils.phone_number_verification import send_phone_number_verification

# from .models import CustomUser, PhoneNumberVerification
# from .serializers import ConfirmPhoneNumberSerializer, CustomUserSerializer, EditProfileSerializer, ChangePasswordSerializer, ChangePhoneNumberSerializer, ResetPasswordSerializer, SendVerificationCodeForResetPasswordSerializer
# from .permissions import IsPhoneNumberVerified

# User = get_user_model()


# class UserProfileViewSet(generics.ListCreateAPIView):
#     """
#     List all users.

#     Use this endpoint to list all users.

#     Parameters:
#     - `phone_number`: Phone of the user
#     """

#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         user = self.request.user
#         user = CustomUser.objects.filter(id=user.id)
#         return user

#     def create(self, request, *args, **kwargs):
#         phone_number = str(request.data["phone_number"])
#         password = request.data["password"]
#         password2 = request.data["password2"]
#         first_name = request.data["first_name"]
#         last_name = request.data["last_name"]
#         data = {
#             "phone_number": phone_number,
#             "password": password,
#             "password2": password2,
#             "first_name": first_name,
#             "last_name": last_name,
#         }
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         # Создаем JWT-токен
#         refresh = RefreshToken.for_user(user)
#         verification = send_phone_number_verification(user.id)
#         user.auth_token = str(refresh.access_token) # Сохраняем токен в поле auth_token

#         # Отправляем письмо для подтверждения регистрации (как в вашем коде)

#         # Возвращаем информацию о пользователе и токене в ответе
#         response_data = {
#             "phone_number": str(user.phone_number),
#             "token": user.auth_token,
#         }

#         return Response(response_data, status=status.HTTP_201_CREATED)


# class SendPhoneNumberVerificationView(generics.GenericAPIView):
#     """
#     Send phone number verification code.
#     Use this endpoint to send phone number verification code.
#     """

#     serializer_class = serializers.Serializer  # Используем стандартный сериализатор

#     def get(self, request):
#         user = request.user
#         if user.is_verified:
#             return Response(
#                 {"detail": "User is already verified"}, status=status.HTTP_200_OK
#             )

#         verification = send_phone_number_verification(user.id)
#         return Response({"detail": "Verification code sent"}, status=status.HTTP_200_OK)


# class PhoneNumberVerificationView(generics.GenericAPIView):
#     """
#     Confirm phone number.

#     Use this endpoint to confirm user phone number.

#     Parameters:
#     - `code`: Code for phone number confirmation
#     """

#     serializer_class = ConfirmPhoneNumberSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         code = request.data["code"]
#         user = CustomUser.objects.get(id=request.user.id)
#         verification = PhoneNumberVerification.objects.filter(user=user, code=code)
#         if verification.exists() and not verification.first().is_expired():
#             user.is_verified = True
#             user.save()
#             return Response(
#                 {"detail": "Phone number confirmed"}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
#             )


# class EditProfileView(generics.GenericAPIView):
#     """
#     Edit profile.

#     Use this endpoint to edit user profile.

#     Parameters:
#     - `first_name`: First name of the user
#     - `last_name`: Last name of the user
#     """

#     serializer_class = EditProfileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]

#     def post(self, request):
#         user = request.user
#         first_name = request.data["first_name"]
#         last_name = request.data["last_name"]
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#         return Response({"detail": "Profile edited"}, status=status.HTTP_200_OK)


# class ChangePasswordView(generics.GenericAPIView):
#     """
#     Change password.

#     Use this endpoint to change user password.

#     Parameters:
#     - `old_password`: Old password of the user
#     - `new_password`: New password of the user
#     """

#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]

#     def is_password_valid(self, password):
#         return len(password) >= 8

#     def do_passwords_match(self, password1, password2):
#         return password1 == password2

#     def post(self, request):
#         user = request.user
#         old_password = request.data.get("old_password")
#         new_password = request.data.get("new_password")
#         new_password2 = request.data.get("new_password2")

#         if old_password == new_password:
#             return self.invalid_password_response("New password must be different")
        
#         if not self.is_password_valid(new_password):
#             return self.invalid_password_response("New password must be at least 8 characters")

#         if not self.do_passwords_match(new_password, new_password2):
#             return self.invalid_password_response("New passwords must match")

#         if user.check_password(old_password):
#             user.set_password(new_password)
#             user.save()
#             return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)
#         else:
#             return self.invalid_password_response("Old password is incorrect")

#     def invalid_password_response(self, detail):
#         return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)


# class SendCodeForChangePhoneNumber(generics.GenericAPIView):
#     """
#     Send code for change phone number.

#     Use this endpoint to send code for change phone number.

#     Parameters:
#     - `phone_number`: Phone number of the user
#     """

#     serializer_class = serializers.Serializer  # Используем стандартный сериализатор
#     permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]

#     def get(self, request):
#         user = request.user
#         verification = send_phone_number_verification(user.id)
#         return Response({"detail": "Verification code sent"}, status=status.HTTP_200_OK)


# class ChangePhoneNumberView(generics.GenericAPIView):
#     """
#     Change phone number.

#     Use this endpoint to change user phone number.

#     Parameters:
#     - `code`: Code for phone number confirmation
#     - `phone_number`: New phone number of the user
#     """

#     serializer_class = ChangePhoneNumberSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPhoneNumberVerified]

#     def post(self, request):
#         user = request.user
#         code = request.data["code"]
#         phone_number = request.data["phone_number"]
#         verification = PhoneNumberVerification.objects.filter(user=user, code=code)
#         if verification.exists() and not verification.first().is_expired():
#             user.phone_number = phone_number
#             user.is_verified = False
#             user.save()
#             return Response(
#                 {"detail": "Phone number changed"}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
#             )


# class SendVerificationCodeForResetPassword(generics.GenericAPIView):
#     """
#     Send verification code for reset password.

#     Use this endpoint to send verification code for reset password.

#     Parameters:
#     - `phone_number`: Phone number of the user
#     """

#     serializer_class = SendVerificationCodeForResetPasswordSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         phone_number = request.data["phone_number"]
#         user = CustomUser.objects.filter(phone_number=phone_number)
#         if user.exists():
#             verification = send_phone_number_verification(user.first().id)
#             return Response(
#                 {"detail": "Verification code sent"}, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {"detail": "User with this phone number does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )



# class GetVerificationCodeForResetPassword(generics.GenericAPIView):
#     """
#     Get verification code for reset password.

#     Use this endpoint to get verification code for reset password.

#     Parameters:
#     - `phone_number`: Phone number of the user
#     - `code`: Code for phone number confirmation
#     """

#     serializer_class = ChangePhoneNumberSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         code = request.data["code"]
#         phone_number = request.data["phone_number"]
#         user = CustomUser.objects.get(phone_number=phone_number)
#         verification = PhoneNumberVerification.objects.filter(user=user, code=code)
#         if verification.exists() and not verification.first().is_expired():
#             return Response({'user_id': user.id}, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
#             )


# class ResetPasswordView(generics.GenericAPIView):
#     """
#     Reset password.

#     Use this endpoint to reset user password.

#     Parameters:
#     - `user_id`: Id of the user
#     - `new_password`: New password of the user
#     - `new_password2`: New password of the user
#     """

#     serializer_class = ResetPasswordSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         user_id = request.data["user_id"]
#         new_password = request.data["new_password"]
#         new_password2 = request.data["new_password2"]

#         if not self.is_password_valid(new_password):
#             return self.invalid_password_response("New password must be at least 8 characters")

#         if not self.do_passwords_match(new_password, new_password2):
#             return self.invalid_password_response("New passwords must match")

#         user = CustomUser.objects.get(id=user_id)
#         user.set_password(new_password)
#         user.save()
#         return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)

#     def invalid_password_response(self, detail):
#         return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

#     def is_password_valid(self, password):
#         return len(password) >= 8

#     def do_passwords_match(self, password1, password2):
#         return password1 == password2