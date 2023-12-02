from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.branches.models import Branch
from apps.storage.serializers import ItemSerializer
from utils.menu import (get_compatibles, get_items_that_can_be_made,
                        get_popular_items)

from .serializers import BranchListSerializer, ChangeBranchSerializer
from .services import get_branch_name_and_id_list


# =============================================================
# Menu Views
# =============================================================
class Menu(APIView):
    """
    View for getting items that can be made.
    """

    permission_classes = [IsAuthenticated]

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
        items = get_items_that_can_be_made(user.branch)
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
        items = get_compatibles(item_id, user.branch)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class BranchesView(ListAPIView):
    """
    View for getting all branches.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BranchListSerializer
    queryset = get_branch_name_and_id_list()

    @swagger_auto_schema(
        operation_summary="Get branches",
        operation_description="Use this endpoint to get all branches.",
        responses={
            200: openapi.Response("Branches"),
        },
    )
    def get(self, request):
        """
        Get all branches.
        """
        queryset = get_branch_name_and_id_list()
        serializer = BranchListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
