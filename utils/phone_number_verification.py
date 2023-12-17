"""
Module for phone number verification
"""

import secrets

import jwt
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from apps.accounts.models import CustomUser, PhoneNumberVerification
from utils.infobip import send_verification_phone_number


def send_phone_number_verification(user_id):
    """
    Create verification code and send it to user phone number
    """
    print("send_phone_number_verification" + str(user_id))
    user = CustomUser.objects.get(id=user_id)
    code = generate_code()
    expiration = timezone.now() + timezone.timedelta(minutes=10)
    verification = PhoneNumberVerification.objects.create(
        code=code, user=user, expiration=expiration
    )
    send_verification_phone_number(code, user.phone_number)
    return verification


def generate_code():
    """
    Generate 4-digit code
    """
    return "".join([str(secrets.randbelow(10)) for _ in range(4)])


def generate_pre_2fa_token(user):
    """
    Generate token for pre 2fa auth
    """
    payload = {
        "id": user.id,
        "phone_number": str(user.phone_number),
        "pre_2fa_auth": True,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def get_user_by_token(token):
    """
    Get user by token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["id"])
        return user
    except CustomUser.DoesNotExist:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    except jwt.InvalidTokenError:
        return None
