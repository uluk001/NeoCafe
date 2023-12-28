from rest_framework.permissions import BasePermission


class IsPhoneNumberVerified(BasePermission):
    """
    Allows access only to verified users.
    """

    message = "Вы не подтвердили свой номер телефона"

    def has_permission(self, request, view):
        return request.user.is_verified


class IsWaiter(BasePermission):
    """
    Allows access only to waiters.
    """

    message = "Вы не являетесь официантом"

    def has_permission(self, request, view):
        return request.user.position == "waiter"


class IsEmployee(BasePermission):
    """
    Allows access only to employees.
    """

    message = "Вы не являетесь сотрудником"

    def has_permission(self, request, view):
        return request.user.position == "waiter" or request.user.position == "barista"
