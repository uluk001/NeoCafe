# from django.contrib.auth import get_user_model
# from django.utils.crypto import get_random_string
# from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()


# class CustomUserSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(required=True)
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)
#     password = serializers.CharField(write_only=True, required=True)
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = (
#             "phone_number",
#             "password",
#             "password2",
#             "first_name",
#             "last_name",
#         )

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError(
#                 {"password": "Пароль не совпадает, попробуйте еще раз"}
#             )
#         return attrs

#     def create(self, validated_data):
#         phone_number = str(validated_data["phone_number"])
#         password = validated_data["password"]
#         first_name = validated_data["first_name"]
#         last_name = validated_data["last_name"]
#         user = User.objects.create_user(
#             phone_number=phone_number,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#         )
#         user.is_active = True
#         user.token_auth = get_random_string(64)
#         user.save()

#         refresh = RefreshToken.for_user(user)
#         return user


# class ConfirmPhoneNumberSerializer(serializers.Serializer):
#     code = serializers.CharField(required=True)


# class EditProfileSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name")


# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     new_password2 = serializers.CharField(required=True)


# class ChangePhoneNumberSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(required=True)
#     code = serializers.CharField(required=True)


# class ResetPasswordSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField(required=True)
#     new_password = serializers.CharField(required=True)
#     new_password2 = serializers.CharField(required=True)


# class SendVerificationCodeForResetPasswordSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(required=True)
