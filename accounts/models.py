from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.crypto import get_random_string

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, name, birth_date, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с заданным номером телефона и паролем.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, name=name, birth_date=birth_date, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, birth_date, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с привилегиями суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, name, birth_date, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField('Phone number', max_length=17, unique=True)
    name = models.CharField('Full name', max_length=255)
    birth_date = models.DateField('Birth date')
    verification_code = models.CharField('Verification Code', max_length=4, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # A staff user; non super-user
    is_superuser = models.BooleanField(default=False)  # A superuser

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'birth_date']

    def set_verification_code(self):
        """
        Генерирует и сохраняет новый случайный четырехзначный код подтверждения.
        """
        self.verification_code = get_random_string(length=4, allowed_chars='0123456789')
        self.save()

    def __str__(self):
        return self.phone
