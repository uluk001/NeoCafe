"""
Web views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .services import (
    accept_order,
    cancel_order,
    get_orders,
    complete_order,
    make_order_ready,
)
from .permissions import IsBarista
from apps.web.serializers import (
    OrderSerializer,
)


# =============================================================
# Branch Views
# =============================================================
class MyBranchIdView(APIView):
    """
    View for getting my branch id.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get my branch id",
        operation_description="Use this endpoint to get my branch id.",
        responses={
            200: openapi.Response("My branch id"),
        },
    )
    def get(self, request, format=None):
        """
        Get my branch id.
        """
        user = request.user
        branch_id = user.branch.id
        return Response({"branch_id": branch_id}, status=status.HTTP_200_OK)


# =============================================================
# Order Views
# =============================================================
class AcceptOrderView(APIView):
    """
    View for accepting order.
    """

    permission_classes = [IsBarista]

    @swagger_auto_schema(
        operation_summary="Accept order",
        operation_description="Use this endpoint to accept order.",
        manual_parameters=[
            openapi.Parameter(
                "order_id",
                openapi.IN_QUERY,
                description="Order id",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response("Order accepted"),
            400: openapi.Response("Order id not found"),
        },
    )
    def get(self, request, format=None):
        """
        Accept order.
        """
        order_id = request.GET.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = accept_order(order_id)
        if not result:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Order accepted"}, status=status.HTTP_200_OK)


class CancelOrderView(APIView):
    """
    View for canceling order.
    """

    permission_classes = [IsBarista]

    @swagger_auto_schema(
        operation_summary="Cancel order",
        operation_description="Use this endpoint to cancel order.",
        manual_parameters=[
            openapi.Parameter(
                "order_id",
                openapi.IN_QUERY,
                description="Order id",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response("Order canceled"),
            400: openapi.Response("Order id not found"),
        },
    )
    def get(self, request, format=None):
        """
        Cancel order.
        """
        order_id = request.GET.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = cancel_order(order_id)
        if not result:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Order canceled"}, status=status.HTTP_200_OK)


class MakeOrderReadyView(APIView):
    """
    View for making order ready.
    """

    permission_classes = [IsBarista]

    @swagger_auto_schema(
        operation_summary="Make order ready",
        operation_description="Use this endpoint to make order ready.",
        manual_parameters=[
            openapi.Parameter(
                "order_id",
                openapi.IN_QUERY,
                description="Order id",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response("Order ready"),
            400: openapi.Response("Order id not found"),
        },
    )
    def get(self, request, format=None):
        """
        Make order ready.
        """
        order_id = request.GET.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = make_order_ready(order_id)
        if not result:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Order ready"}, status=status.HTTP_200_OK)


class CompleteOrderView(APIView):
    """
    View for completing order.
    """

    @swagger_auto_schema(
        operation_summary="Complete order",
        operation_description="Use this endpoint to complete order.",
        manual_parameters=[
            openapi.Parameter(
                "order_id",
                openapi.IN_QUERY,
                description="Order id",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response("Order completed"),
            400: openapi.Response("Order id not found"),
        },
    )
    def get(self, request, format=None):
        """
        Complete order.
        """
        order_id = request.GET.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = complete_order(order_id)
        if not result:
            return Response(
                {"error": "Order id not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Order completed"}, status=status.HTTP_200_OK)


class GetInProcessTakeawayOrdersView(APIView):
    """
    View for getting in process orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get in process orders",
        operation_description="Use this endpoint to get in process orders.",
        responses={
            200: openapi.Response("In process orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get in process orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=False,
            status="in_progress",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetCanceledTakeawayOrdersView(APIView):
    """
    View for getting canceled takeaway orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get canceled takeaway orders",
        operation_description="Use this endpoint to get canceled takeaway orders.",
        responses={
            200: openapi.Response("Canceled takeaway orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get canceled takeaway orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=False,
            status="canceled",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetReadyTakeawayOrdersView(APIView):
    """
    View for getting ready takeaway orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get ready takeaway orders",
        operation_description="Use this endpoint to get ready takeaway orders.",
        responses={
            200: openapi.Response("Ready takeaway orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get ready takeaway orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=False,
            status="ready",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetCompletedTakeawayOrdersView(APIView):
    """
    View for getting completed takeaway orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get completed takeaway orders",
        operation_description="Use this endpoint to get completed takeaway orders.",
        responses={
            200: openapi.Response("Completed takeaway orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get completed takeaway orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=False,
            status="completed",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetInProcessInstitutionOrdersView(APIView):
    """
    View for getting in process institution orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get in process institution orders",
        operation_description="Use this endpoint to get in process institution orders.",
        responses={
            200: openapi.Response("In process institution orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get in process institution orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=True,
            status="in_progress",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetCanceledInstitutionOrdersView(APIView):
    """
    View for getting canceled institution orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get canceled institution orders",
        operation_description="Use this endpoint to get canceled institution orders.",
        responses={
            200: openapi.Response("Canceled institution orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get canceled institution orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=True,
            status="canceled",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetReadyInstitutionOrdersView(APIView):
    """
    View for getting ready institution orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get ready institution orders",
        operation_description="Use this endpoint to get ready institution orders.",
        responses={
            200: openapi.Response("Ready institution orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get ready institution orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=True,
            status="ready",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


class GetCompletedInstitutionOrdersView(APIView):
    """
    View for getting completed institution orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get completed institution orders",
        operation_description="Use this endpoint to get completed institution orders.",
        responses={
            200: openapi.Response("Completed institution orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get completed institution orders.
        """
        user = request.user
        branch_id = user.branch.id
        orders = get_orders(
            branch_id=branch_id,
            in_an_institution=True,
            status="completed",
        )
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)
