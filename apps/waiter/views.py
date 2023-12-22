from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.waiter.services import (
    get_tables_availability, get_occupied_tables,
    get_table_order_details,
    get_orders_in_institution,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.customers.serializers import OrderSerializer
from apps.waiter.serializers import WaiterOpenedOrdersSerializer

class GetTableAvailibilityView(APIView):
    """
    View for table availibility.
    """

    @swagger_auto_schema(
        operation_summary="Gets table availibility.",
        operation_description="User must be authenticated.",
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'free_tables': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description='List of free tables',
                    ),
                    'occupied_tables': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description='List of occupied tables',
                    ),
                },
            ),
        },
    )
    def get(self, request):
        """
        Gets table availibility.
        """
        return Response({
            'tables': get_tables_availability(request.user.branch_id),
        })


class TableDetailView(APIView):
    """
    View for table detail.
    """
    
    @swagger_auto_schema(
        operation_summary="Gets table details.",
        operation_description="User must be authenticated.",
        manual_parameters=[
            openapi.Parameter(
                name='table_number',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Table number',
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'order': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'items': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_OBJECT),
                                description='List of order items',
                            ),
                            'total_price': openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                description='Total price of order',
                            ),
                            'spent_bonus_points': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Spent bonus points',
                            ),
                            'in_an_institution': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Is order in an institution',
                            ),
                            'table_number': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Table number',
                            ),
                        },
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Table not found',
                    ),
                },
            ),
        },
    )
    def get(self, request):
        """
        Gets table details.
        """

        table_number = request.query_params.get('table_number')

        order = get_table_order_details(request.user.branch_id, table_number)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            'order': OrderSerializer(order).data,
        })


class WaiterOpenedOrdersView(APIView):
    """
    View for waiter opened orders.
    """

    @swagger_auto_schema(
        operation_summary="Gets waiter opened orders.",
        operation_description="User must be authenticated.",
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'orders': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        description='List of orders',
                    ),
                },
            ),
        },
    )
    def get(self, request):
        """
        Gets waiter opened orders.
        """
        return Response({
            'orders': WaiterOpenedOrdersSerializer(get_orders_in_institution(request.user.branch_id), many=True).data,
        })
