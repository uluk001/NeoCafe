"""
Module for ordering views.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.ordering.serializers import OrderSerializer
from apps.ordering.services import create_order
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CreateOrderView(APIView):
    """
    View for orders.
    """

    @swagger_auto_schema(
        operation_summary="Creates order.",
        operation_description="User must be authenticated, items must be not empty, total price must be greater than 0, spent bonus points must be greater than or equal to 0.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'total_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Total price of the order'),
                'spent_bonus_points': openapi.Schema(type=openapi.TYPE_INTEGER, description='Bonus points spent on the order'),
                'in_an_institution': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the order is made in an institution'),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'item': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the item'),
                            'is_ready_made_product': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether the item is a ready-made product'),
                            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the item'),
                        }
                    ),
                    description='List of items in the order',
                ),
            },
            required=['total_price', 'spent_bonus_points', 'items'],
        ),
    )

    def post(self, request):
        """
        Creates order.
        """
        return Response(
            OrderSerializer(
                create_order(
                    user_id=request.user.id,
                    total_price=request.data['total_price'],
                    items=request.data['items'],
                    spent_bonus_points=request.data['spent_bonus_points'],
                    in_an_institution=request.data['in_an_institution'],
                )
            ).data,
            status=status.HTTP_201_CREATED,
        )