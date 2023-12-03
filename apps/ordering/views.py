"""
Module for ordering views.
"""
from apps.ordering.serializers import TestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.menu import check_if_items_can_be_made
from apps.storage.models import Item


class TestView(APIView):
    """
    Test view.
    """
    serializer_class = TestSerializer

    def post(self, request):
        """
        Test post method.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        branch_id = data["branch_id"]
        item_id = data["id"]
        quantity = data["quantity"]
        if check_if_items_can_be_made(branch_id=branch_id, item_id=item_id, quantity=quantity):
            return Response("Item can be made.", status=status.HTTP_200_OK)
        return Response("Item can't be made.", status=status.HTTP_400_BAD_REQUEST)
