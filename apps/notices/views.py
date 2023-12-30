from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BaristaNotification, AdminNotification
from .services import (
    delete_baristas_notification,
    delete_client_notification,
    clear_waiter_notifications,
    delete_admin_notification,
    clear_admin_notifications,
)


class DeleteBaristaNotificationView(APIView):
    """
    Endpoint for deleting notification.

    Use this endpoint to delete notification.

    Parameters:
    id (int): The id of the notification.
    """

    def get(self, request, format=None):
        """
        Delete notification.
        """
        id = request.query_params.get("id")
        if delete_baristas_notification(id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteClientNotificationView(APIView):
    """
    Endpoint for deleting notification.

    Use this endpoint to delete notification.

    Parameters:
    id (int): The id of the notification.
    """

    def get(self, request, format=None):
        """
        Delete notification.
        """
        id = request.query_params.get("id")
        if delete_client_notification(id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClearWaiterNotificationsView(APIView):
    """
    Endpoint for deleting notifications.

    Use this endpoint to delete notifications.

    Parameters:
    waiter_id (int): The id of the waiter.
    """

    def get(self, request, format=None):
        """
        Delete notifications.
        """
        waiter_id = request.query_params.get("waiter_id")
        if clear_waiter_notifications(waiter_id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteAdminNotificationView(APIView):
    """
    Endpoint for deleting notification.

    Use this endpoint to delete notification.

    Parameters:
    id (int): The id of the notification.
    """

    def get(self, request, format=None):
        """
        Delete notification.
        """
        id = request.query_params.get("id")
        if delete_admin_notification(id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClearAdminNotificationsView(APIView):
    """
    Endpoint for deleting notifications.

    Use this endpoint to delete notifications.
    """

    def get(self, request, format=None):
        """
        Delete notifications.
        """
        if clear_admin_notifications():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
