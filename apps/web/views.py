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

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Accept order",
        operation_description="Use this endpoint to accept order.",
        responses={
            200: openapi.Response("Order accepted"),
            400: openapi.Response("Order not found"),
        },
    )

    def get(self, request, format=None):
        """
        Accept order.
        """
        order_id = request.GET.get("order_id")
        if not order_id:
            return Response(
                {"message": "Order id not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "Order accepted"}, status=status.HTTP_200_OK)