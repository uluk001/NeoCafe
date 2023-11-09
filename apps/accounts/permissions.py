from rest_framework.permissions import BasePermission


class IsPhoneNumberVerified(BasePermission):
    """
    Allows access only to verified users.
    """
    message = "Вы не подтвердили свой номер телефона"

    def has_permission(self, request, view):
        return request.user.is_verified