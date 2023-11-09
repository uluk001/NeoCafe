from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from apps.branches.models import Branch
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name=None, last_name=None, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number,
            first_name="Admin",
            last_name="User",
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    POSITIONS = (
        ("barista", "Barista"),
        ("waiter", "Waiter"),
        ("client", "Client")
    )

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=128)
    token_auth = models.CharField(max_length=64, blank=True, null=True)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, null=True)
    bonus = models.IntegerField(default=0)
    position = models.CharField(max_length=255, choices=POSITIONS, default="client")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions",
        related_query_name="customuser",
    )

    def __str__(self):
        return f"CustomUser object for {self.phone_number}"


class PhoneNumberVerification(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="phone_number_verifications"
    )
    expiration = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PhoneNumberVerification object for {self.user.phone_number}"

    def is_expired(self):
        return True if now() >= self.expiration else False
