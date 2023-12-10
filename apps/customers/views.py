from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import (
    OrderingFilter, SearchFilter,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.branches.models import Branch
from apps.storage.serializers import ItemSerializer
from utils.menu import (
    get_compatibles, item_search,
    get_popular_items, combine_items_and_ready_made_products,
)
from .serializers import ChangeBranchSerializer


# =============================================================
# Menu Views
# =============================================================
class Menu(APIView):
    """
    View for getting items that can be made.
    """

    @swagger_auto_schema(
        operation_summary="Get menu",
        operation_description="Use this endpoint to get items that can be made.",
        responses={
            200: openapi.Response("Items that can be made"),
        },
    )
    def get(self, request, format=None):
        """
        Get items that can be made.
        """
        user = request.user
        category_id = request.GET.get("category_id")
        items = combine_items_and_ready_made_products(user.branch.id, category_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularItemsView(APIView):
    """
    View for getting popular items.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get popular items",
        operation_description="Use this endpoint to get popular items.",
        responses={
            200: openapi.Response("Popular items"),
        },
    )
    def get(self, request, format=None):
        """
        Get popular items.
        """
        user = request.user
        items = get_popular_items(user.branch)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompatibleItemsView(APIView):
    """
    View for getting compatible items.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get compatible items",
        operation_description="Use this endpoint to get compatible items.",
        responses={
            200: openapi.Response("Compatible items"),
        },
    )
    def get(self, request, item_id, format=None):
        """
        Get compatible items.
        """
        user = request.user
        items = get_compatibles(item_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemSearchView(APIView):
    """
    View to search items.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Search items.
        """
        user = request.user
        query = request.GET.get("query")
        items = item_search(query, user.branch.id)
        return Response(items, status=status.HTTP_200_OK)


# =============================================================
# Branch Views
# =============================================================
class ChangeBranchView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeBranchSerializer

    @swagger_auto_schema(
        operation_summary="Change branch",
        operation_description="Use this endpoint to change branch. You need to provide branch id.",
        request_body=ChangeBranchSerializer,
        responses={
            200: openapi.Response("Branch changed successfully"),
            400: openapi.Response("Invalid data"),
        },
    )
    def post(self, request, format=None):
        """
        Change branch.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            branch_id = serializer.validated_data.get("branch_id")
            user = request.user
            branch = Branch.objects.get(id=branch_id)
            user.branch = branch
            user.save()
            return Response(
                {"message": "Branch changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================
# Profile Views
# =============================================================
class MyBonusesView(APIView):
    """
    View for getting user's bonuses.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get bonuses",
        operation_description="Use this endpoint to get user's bonuses.",
        responses={
            200: openapi.Response("User's bonuses"),
        },
    )
    def get(self, request, format=None):
        """
        Get user's bonuses.
        """
        user = request.user
        return Response({"bonus": user.bonus}, status=status.HTTP_200_OK)