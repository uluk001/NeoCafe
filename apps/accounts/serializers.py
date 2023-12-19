import datetime

import phonenumbers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from phonenumbers import NumberParseException, is_valid_number
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.branches.models import Branch

User = get_user_model()


def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)
    except NumberParseException:
        raise serializers.ValidationError("Введите корректный номер телефона")

    if not is_valid_number(phone_number):
        raise serializers.ValidationError(
            "Номер телефона не соответствует мировому стандарту"
        )
    return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """

    phone_number = serializers.CharField(
        required=True, validators=[validate_phone_number]
    )
    first_name = serializers.CharField()
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "birth_date",
        )

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        phone_number = str(validated_data["phone_number"])
        first_name = validated_data["first_name"]
        birth_date = validated_data.get("birth_date")
        if birth_date > datetime.date.today():
            raise serializers.ValidationError(
                {"message": "Дата рождения не может быть больше текущей даты"}
            )
        try:
            user = User.objects.create_user(
                phone_number=phone_number,
                first_name=first_name,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {"message": "Пользователь с таким номером телефона уже существует"}
            )
        user.birth_date = birth_date
        user.is_active = True
        user.token_auth = get_random_string(64)
        default_branch = Branch.objects.all().first()
        user.branch = default_branch
        user.save()

        refresh = RefreshToken.for_user(user)
        return user


class ClientConfirmPhoneNumberSerializer(serializers.Serializer):
    """
    Serializer for confirming phone number
    """

    code = serializers.CharField(required=True)


class ClientBirthDateSerializer(serializers.Serializer):
    """
    Serializer for birth date
    """

    birth_date = serializers.DateField(required=True)


class ClientEditProfileSerializer(serializers.Serializer):
    """
    Serializer for editing profile
    """

    first_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(
        required=True, validators=[validate_phone_number]
    )
    birth_date = serializers.DateField(required=True)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login
    """

    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)


class ChangePhoneNumberSerializer(serializers.Serializer):
    """
    Serializer for changing phone number
    """

    phone_number = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for reset password
    """

    user_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)


class SendVerificationCodeForResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for sending verification code for reset password
    """

    phone_number = serializers.CharField(required=True)


class AdminLoginSerializer(serializers.Serializer):
    """
    Serializer for admin login
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LoginForClientSerializer(serializers.Serializer):
    """
    Serializer for client login
    """

    phone_number = serializers.CharField(required=True)


class WaiterLoginSerializer(serializers.Serializer):
    """
    Serializer for waiter login
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for profile
    """

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "username",
            "birth_date",
            "bonus",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.position not in ['barista', 'waiter']:
            representation.pop('bonus')
        return representation


class UpdateWaiterProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birth_date",
        )
