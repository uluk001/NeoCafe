"""
Module for ordering views.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.menu import check_if_items_can_be_made
from apps.storage.models import Item
from apps.ordering.serializers import OrderSerializer
from apps.ordering.services import create_order


class CreateOrderView(APIView):
    """
    View for orders.
    """
    
    def post(self, request):
        """
        Creates order.
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            total_price = serializer.validated_data['total_price']
            spent_bonus_points = serializer.validated_data['spent_bonus_points']
            items = serializer.validated_data['items']

            order = create_order(
                user_id=request.user.id,
                total_price=total_price,
                items=items,
                spent_bonus_points=spent_bonus_points,
            )

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
