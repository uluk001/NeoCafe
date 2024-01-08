from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ordering.models import Order
from apps.branches.models import Branch
from apps.storage.models import Item, ReadyMadeProduct
from utils.menu import (
    get_compatibles,
    item_search,
    get_popular_items,
    combine_items_and_ready_made_products,
    check_if_items_can_be_made,
    check_if_ready_made_product_can_be_made,
)
from apps.storage.serializers import ItemSerializer
from .serializers import (
    ChangeBranchSerializer,
    ExtendedItemSerializer,
    CheckIfItemCanBeMadeSerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserOrdersSerializer,
    MenuItemDetailSerializer,
)


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
        serializer = ExtendedItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuItemDetailView(APIView):
    """
    View for getting menu item detail.
    """

    @swagger_auto_schema(
        operation_summary="Получить детальный список пунктов меню",
        operation_description="Используйте этот эндпоинт для получения детального списка пунктов меню. Используйте параметр is_ready_made_product для получения детального списка готовых продуктов или обычных пунктов меню, по умолчанию is_ready_made_product = false. false (Обычные пункты меню) если is_ready_made_product = true (Готовые продукты).\nНапример:\n/customers/menu/1/?is_ready_made_product=true - получить детальный список готовых продуктов с id = 1\n /customers/menu/1?is_ready_made_product=false - получить детальный список обычных пунктов меню с id = 1",
        responses={
            200: openapi.Response("Menu item detail"),
        },
        manual_parameters=[
            openapi.Parameter(
                "is_ready_made_product",
                openapi.IN_QUERY,
                description="Is ready made product",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
        
    def get(self, request, item_id, format=None):
        """
        Get menu item detail.
        """
        is_ready_made_product = request.GET.get("is_ready_made_product", False)
        is_ready_made_product = True if is_ready_made_product == "true" else False

        # Проверка валидности item_id
        try:
            item_id = int(item_id)
        except ValueError:
            return Response(
                {"message": "Invalid item_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            item = (
                Item.objects.get(id=item_id)
                if not is_ready_made_product
                else ReadyMadeProduct.objects.get(id=item_id)
            )
        except Item.DoesNotExist:
            return Response(
                {"message": "Item does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MenuItemDetailSerializer(
            item,
            context={"id": item_id, "is_ready_made_product": is_ready_made_product},
        )
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
        serializer = MenuItemDetailSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompatibleItemsView(APIView):
    """
    View for getting compatible items.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get compatible items",
        operation_description="Use this endpoint to get compatible items. In order to get compatible items you need to provide item id and is_ready_made_product parameter. is_ready_made_product = true if item is ready made product, false if item is not ready made product.\nFor example:\n/customers/compatible-items/1/?is_ready_made_product=true - get compatible ready-made products with id = 1\n/customers/compatible-items/1/?is_ready_made_product=false - get compatible regular menu items with id = 1",
        responses={
            200: openapi.Response("Compatible items"),
        },
        manual_parameters=[
            openapi.Parameter(
                "is_ready_made_product",
                openapi.IN_QUERY,
                description="Is ready made product",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
    def get(self, request, item_id, format=None):
        """
        Get compatible items.
        """
        is_ready_made_product = request.GET.get("is_ready_made_product", False)
        is_ready_made_product = True if is_ready_made_product == "true" else False
        branch_id = request.user.branch.id
        items = get_compatibles(item_id, is_ready_made_product, branch_id)
        serializer = MenuItemDetailSerializer(items, many=True)
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


class CheckIfItemCanBeMadeView(APIView):
    """
    View for checking if item can be made.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CheckIfItemCanBeMadeSerializer

    @swagger_auto_schema(
        operation_summary="Check if item can be made",
        operation_description="Use this endpoint to check if item can be made.",
        responses={
            200: openapi.Response("Item can be made"),
            400: openapi.Response("Item can't be made"),
        },
        manual_parameters=[
            openapi.Parameter(
                "item_id",
                openapi.IN_QUERY,
                description="Item id",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "quantity",
                openapi.IN_QUERY,
                description="Quantity",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "is_ready_made_product",
                openapi.IN_QUERY,
                description="Is ready made product",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
    def post(self, request, format=None):
        """
        Check if item can be made.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data.get("item_id")
            quantity = serializer.validated_data.get("quantity")
            is_ready_made_product = serializer.validated_data.get(
                "is_ready_made_product"
            )
            user = request.user
            if is_ready_made_product:
                if check_if_ready_made_product_can_be_made(
                    item_id, user.branch.id, quantity
                ):
                    return Response(
                        {"message": "Item can be made."},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"message": "Item can't be made."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if check_if_items_can_be_made(item_id, user.branch.id, quantity):
                return Response(
                    {"message": "Item can be made."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Item can't be made."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class MyIdView(APIView):
    """
    View for getting user's id.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get id",
        operation_description="Use this endpoint to get user's id.",
        responses={
            200: openapi.Response("User's id"),
        },
    )
    def get(self, request, format=None):
        """
        Get user's id.
        """
        user = request.user
        return Response({"id": user.id}, status=status.HTTP_200_OK)


# =============================================================
# Order Views
# =============================================================
class MyOrdersView(APIView):
    """
    View for getting user's orders.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get orders",
        operation_description="Use this endpoint to get user's orders.",
        responses={
            200: openapi.Response("User's orders"),
        },
    )
    def get(self, request, format=None):
        """
        Get user's orders.
        """
        user = request.user
        serializer = UserOrdersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyOrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
