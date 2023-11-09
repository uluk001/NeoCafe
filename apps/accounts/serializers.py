from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number


User = get_user_model()


def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)
    except NumberParseException:
        raise serializers.ValidationError("Введите корректный номер телефона")

    if not is_valid_number(phone_number):
        raise serializers.ValidationError("Номер телефона не соответствует мировому стандарту")
    return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, validators=[validate_phone_number])
    first_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
        )

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        phone_number = str(validated_data["phone_number"])
        first_name = validated_data["first_name"]
        user = User.objects.create_user(
            phone_number=phone_number,
            first_name=first_name,
        )
        user.is_active = True
        user.token_auth = get_random_string(64)
        user.save()

        refresh = RefreshToken.for_user(user)
        return user


class ClientConfirmPhoneNumberSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class ClientBirthDateSerializer(serializers.Serializer):
    birth_date = serializers.DateField(required=True)


class ClientEditProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True, validators=[validate_phone_number])
    birth_date = serializers.DateField(required=True)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)


class ChangePhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)


class SendVerificationCodeForResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
