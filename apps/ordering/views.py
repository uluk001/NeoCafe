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
                            'ready_made_product': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the ready made product'),
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
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            total_price = serializer.validated_data['total_price']
            spent_bonus_points = serializer.validated_data['spent_bonus_points']
            items = serializer.validated_data['items']
            in_an_institution = serializer.validated_data['in_an_institution']
            if not items:
                return Response({"items": ["This field must not be empty."]}, status=status.HTTP_400_BAD_REQUEST)

            order = create_order(
                user_id=request.user.id,
                total_price=total_price,
                items=items,
                spent_bonus_points=spent_bonus_points,
                in_an_institution=in_an_institution,
            )
            if not order:
                return Response({"items": ["Not enough ingredients."]}, status=status.HTTP_400_BAD_REQUEST)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
