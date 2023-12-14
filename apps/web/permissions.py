from rest_framework import permissions


class IsBarista(permissions.BasePermission):
    """
    Permission for barista.
    """

    def has_permission(self, request, view):
        return request.user.position == "barista"
