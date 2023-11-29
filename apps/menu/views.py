from apps.storage.serializers import ItemSerializer

from utils.menu import get_items_that_can_be_made
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, GenericAPIView


class Menu(APIView):
    """
    View for getting items that can be made.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Get items that can be made.
        """
        user = request.user
        items = get_items_that_can_be_made(user.branch)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
