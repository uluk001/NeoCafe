from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BaristaNotification
from .services import delete_baristas_notification, delete_client_notification


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
        id = request.query_params.get('id')
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
        id = request.query_params.get('id')
        if delete_client_notification(id):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)