"""
Views for storage app
"""
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import CustomUser
from apps.storage.filters import (
    EmployeeFilter, IngredientFilter, ItemFilter,
    ReadyMadeProductFilter)
from apps.storage.serializers import (
    AvailableAtTheBranchSerializer, CategorySerializer,
    CreateIngredientSerializer, CreateItemSerializer,
    CreateReadyMadeProductSerializer, EmployeeCreateSerializer,
    EmployeeSerializer, EmployeeUpdateSerializer, IngredientDetailSerializer,
    IngredientQuantityUpdateSerializer, IngredientSerializer, ItemSerializer,
    PutImageToItemSerializer, ReadyMadeProductAvailableAtTheBranchSerializer,
    ReadyMadeProductSerializer, ScheduleUpdateSerializer,
    UpdateIngredientSerializer, UpdateItemSerializer,
    UpdateReadyMadeProductSerializer, PutImageToReadyMadeProductSerializer,
)
from apps.storage.services import (
    delete_employee_schedule_by_employee,
    get_a_list_of_ingredients_and_their_quantities_in_specific_branch,
    get_available_at_the_branch, get_categories, get_employees,
    get_ingrediants, get_items, get_low_stock_ingredients_in_branch,
    get_ready_made_products, get_specific_category, get_specific_employee,
)


# =====================================================================
# CATEGORY VIEWS
# =====================================================================
class CreateCategoryView(generics.CreateAPIView):
    """
    Create category view for admins.
    """

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Create category",
        operation_description="Use this method to create a category. Only admins can create categories",
        request_body=manual_request_schema,
        responses={201: "Category created successfully"},
    )
    def post(self, request):
        """
        Create category method.
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category created successfully"}, status=201)
        return Response(serializer.errors, status=400)

    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer


class DestroyCategoryView(generics.DestroyAPIView):
    """
    Delete category view for admins.
    """

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    @swagger_auto_schema(
        operation_summary="Delete category",
        operation_description="Use this method to delete a category. Only admins can delete categories",
        responses={
            200: openapi.Response(
                "Category deleted successfully", manual_response_schema
            )
        },
    )
    def delete(self, request, pk):
        """
        Delete category method.
        """
        category = get_specific_category(pk)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=200)

    queryset = get_categories()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ListCategoryView(generics.ListAPIView):
    """
    List category view.
    """

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get categories",
        operation_description="Use this method to get all categories",
        responses={200: openapi.Response("Categories list", list_response_schema)},
    )
    def get(self, request):
        """
        Get categories method.
        """
        categories = get_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    queryset = get_categories()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateCategoryView(generics.UpdateAPIView):
    """
    Update category view for admins.
    """

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Update category",
        operation_description="Use this method to update a category. Only admins can update categories",
        request_body=manual_request_schema,
        responses={
            200: openapi.Response("Category updated successfully", CategorySerializer)
        },
    )
    def put(self, request, pk):
        """
        Update category method.
        """
        category = get_specific_category(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category updated successfully"}, status=200)
        return Response(serializer.errors, status=400)

    queryset = get_categories()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# =====================================================================
# EMPLOYEE VIEWS
# =====================================================================
class CreateEmployeeView(generics.CreateAPIView):
    """
    Create employee view.
    """

    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Create employee",
        operation_description="Use this method to create an employee. Only admins can create employees.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Alixandro_barman"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, example="123456789"
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Алихандро"
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["barista", "waiter"],
                    example="barista",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", example="1997-05-31"
                ),
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, example="+996555231234"
                ),
                "branch": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Branch id where employee works",
                    example=1,
                ),
                "workdays": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "workday": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Workday number. 1 - Monday, 2 - Tuesday, etc.",
                                example=1,
                            ),
                            "start_time": openapi.Schema(
                                type=openapi.TYPE_STRING, example="09:00"
                            ),
                            "end_time": openapi.Schema(
                                type=openapi.TYPE_STRING, example="17:00"
                            ),
                        },
                    ),
                ),
            },
        ),
        responses={201: "Employee created successfully"},
    )
    def post(self, request):
        """
        Create employee method.
        """
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee created successfully"}, status=201)
        return Response(serializer.errors, status=400)


class EmployeeDestroyView(generics.DestroyAPIView):
    """
    Delete employee view.
    """

    queryset = CustomUser.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAdminUser]

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    @swagger_auto_schema(
        operation_summary="Delete employee",
        operation_description="Use this method to delete an employee. Only admins can delete employees",
        responses={
            200: openapi.Response(
                "Employee deleted successfully", manual_response_schema
            )
        },
    )
    def delete(self, request, pk):
        """
        Delete employee method.
        """
        employee = get_specific_employee(pk)
        employee_schedule = delete_employee_schedule_by_employee(employee)
        employee.delete()

        return Response({"message": "Employee deleted successfully"}, status=200)


class EmployeeListView(generics.ListAPIView):
    """
    List employee view. Only admins can get employees. You can filter employees by name. Example: /storage/employees/?name=Alixandro
    """

    queryset = get_employees()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "position": openapi.Schema(type=openapi.TYPE_STRING),
            "birth_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "branch": openapi.Schema(type=openapi.TYPE_INTEGER),
            "schedule": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "workdays": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "workday": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "start_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="time"
                                ),
                                "end_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="time"
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get employees",
        operation_description="Use this method to get all employees",
        responses={200: openapi.Response("Employees list", list_response_schema)},
    )
    def get(self, request):
        """
        Get employees method.
        """
        return super().get(request)


class EmployeeDetailView(generics.RetrieveAPIView):
    """
    Employee detail view. Only admins can get employee details.
    """

    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = get_employees()

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "position": openapi.Schema(type=openapi.TYPE_STRING),
            "birth_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "branch": openapi.Schema(type=openapi.TYPE_INTEGER),
            "schedule": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "workdays": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "workday": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "start_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="time"
                                ),
                                "end_time": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="time"
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Get specific employee",
        operation_description="Use this endpoint to get a specific employee",
        responses={200: openapi.Response("Employees object", manual_response_schema)},
    )
    def get(self, request, pk=None):
        """
        Get specific employee method.
        """
        return super().get(request, pk)


class EmployeeUpdateView(generics.UpdateAPIView):
    """
    Update employee view.
    """

    queryset = CustomUser.objects.all()
    serializer_class = EmployeeUpdateSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "position": openapi.Schema(type=openapi.TYPE_STRING),
            "birth_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "branch": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    )

    @swagger_auto_schema(
        operation_summary="Update employee",
        operation_description="Use this method to update an employee",
        request_body=manual_request_schema,
        responses={
            200: openapi.Response(
                "Employee updated successfully", EmployeeUpdateSerializer
            )
        },
    )
    def put(self, request, pk):
        employee = CustomUser.objects.get(pk=pk)
        serializer = EmployeeUpdateSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee updated successfully"}, status=200)
        return Response(serializer.errors, status=400)


class ScheduleUpdateView(generics.UpdateAPIView):
    """
    Update employee schedule view.
    """

    permission_classes = [permissions.IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = ScheduleUpdateSerializer
    lookup_field = "pk"

    def get_serializer_context(self):
        """
        Get serializer context.
        """
        context = super().get_serializer_context()
        context["user_id"] = self.kwargs.get("pk")
        return context


# =====================================================================
# INGREDIENT VIEWS
# =====================================================================
class CreateIngredientView(generics.CreateAPIView):
    """
    Create ingredient view.
    """

    queryset = get_ingrediants()
    serializer_class = CreateIngredientSerializer
    permission_classes = [permissions.IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "measurement_unit": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["g", "ml", "l", "kg"],
            ),
            "available_at_branches": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "branch": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "minimal_limit": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Create ingredient",
        operation_description="Use this method to create an ingredient. Only admins can create ingredients",
        request_body=manual_request_schema,
        responses={201: "Ingredient created successfully"},
    )
    def post(self, request):
        """
        Create ingredient method.
        """
        serializer = CreateIngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ingredient created successfully"}, status=201)
        return Response(serializer.errors, status=400)


class UpdateIngredientView(generics.UpdateAPIView):
    """
    Update ingredient view.
    """

    queryset = get_ingrediants()
    serializer_class = UpdateIngredientSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "measurement_unit": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["g", "ml", "l", "kg"],
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Update ingredient",
        operation_description="Use this method to update an ingredient",
        request_body=manual_request_schema,
        responses={
            200: openapi.Response(
                "Ingredient updated successfully", UpdateIngredientSerializer
            )
        },
    )
    def put(self, request, pk):
        ingredient = get_ingrediants().filter(pk=pk).first()
        serializer = UpdateIngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ingredient updated successfully"}, status=200)
        return Response(serializer.errors, status=400)


class IngredientListView(APIView):
    """
    List ingredient view. You can filter ingredients by name. Example: /storage/ingredients/?name=Молоко
    """

    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IngredientFilter

    def get(self, request):
        """
        Get ingredients method.
        """
        ingredients = get_ingrediants()
        filtered_ingredients = self.filterset_class(request.GET, queryset=ingredients)
        serializer = IngredientSerializer(filtered_ingredients.qs, many=True)
        return Response(serializer.data)


class IngredientDestroyView(generics.DestroyAPIView):
    """
    Delete ingredient view.
    """

    queryset = get_ingrediants()
    serializer_class = IngredientSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAdminUser]

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    @swagger_auto_schema(
        operation_summary="Delete ingredient",
        operation_description="Use this method to delete an ingredient. Only admins can delete ingredients",
        responses={
            200: openapi.Response(
                "Ingredient deleted successfully", manual_response_schema
            )
        },
    )
    def delete(self, request, pk):
        """
        Delete ingredient method.
        """
        ingredient = get_ingrediants().filter(pk=pk).first()
        ingredient.delete()
        return Response({"message": "Ingredient deleted successfully"}, status=200)


class IngredientDetailView(generics.RetrieveAPIView):
    """
    Ingredient detail view.
    """

    queryset = get_ingrediants()
    serializer_class = IngredientDetailSerializer
    lookup_field = "pk"
    permission_classes = [permissions.IsAdminUser]


class IngredientQuantityUpdateView(generics.UpdateAPIView):
    """
    Class for updating ingredient quantity.
    """

    queryset = get_available_at_the_branch()
    serializer_class = IngredientQuantityUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


class InredientDestroyFromBranchView(generics.DestroyAPIView):
    """
    Class for deleting ingredient from branch.
    """

    queryset = get_available_at_the_branch()
    serializer_class = AvailableAtTheBranchSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Delete ingredient from branch",
        operation_description="Use this method to delete an ingredient from branch. Only admins can delete ingredients from branch",
        responses={
            200: openapi.Response(
                "Ingredient deleted successfully", AvailableAtTheBranchSerializer
            )
        },
    )
    def delete(self, request, pk):
        """
        Delete ingredient from branch method.
        """
        ingredient = get_available_at_the_branch().filter(pk=pk).first()
        ingredient.delete()
        return Response({"message": "Ingredient deleted successfully"}, status=200)


class IngredientQuantityInBranchView(generics.ListAPIView):
    """
    Class for getting ingredient quantity in branch.
    """

    queryset = get_available_at_the_branch()
    permission_classes = [permissions.IsAdminUser]

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "ingredient": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "measurement_unit": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=["g", "ml", "l", "kg"],
                    ),
                    "minimal_limit": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "date_of_arrival": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date"
                    ),
                },
            ),
            "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get ingredient quantity in branch",
        operation_description="Use this method to get ingredient quantity in branch",
        responses={
            200: openapi.Response("Ingredient quantity in branch", list_response_schema)
        },
    )
    def get(self, request, pk):
        """
        Get ingredient quantity in branch method.
        """
        ingredients = get_a_list_of_ingredients_and_their_quantities_in_specific_branch(
            branch_id=pk
        )
        return Response(ingredients, status=200)


class LowStockIngredientBranchView(generics.ListAPIView):
    """
    Class for getting low stock ingredients in branch.
    """

    queryset = get_available_at_the_branch()
    permission_classes = [permissions.IsAdminUser]

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "ingredient": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "measurement_unit": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=["g", "ml", "l", "kg"],
                    ),
                    "minimal_limit": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "date_of_arrival": openapi.Schema(
                        type=openapi.TYPE_STRING, format="date"
                    ),
                },
            ),
            "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get low stock ingredients in branch",
        operation_description="Use this method to get low stock ingredients in branch",
        responses={
            200: openapi.Response(
                "Low stock ingredients in branch", list_response_schema
            )
        },
    )
    def get(self, request, pk):
        """
        Get low stock ingredients in branch method.
        """
        ingredients = get_low_stock_ingredients_in_branch(branch_id=pk)
        return Response(ingredients, status=200)


# =====================================================================
# ITEM VIEWS
# =====================================================================
class CreateItemView(generics.CreateAPIView):
    """
    Class for creating items.
    """

    queryset = get_ingrediants()
    serializer_class = CreateItemSerializer

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "category": openapi.Schema(type=openapi.TYPE_STRING),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "is_available": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "composition": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "ingredient": openapi.Schema(type=openapi.TYPE_STRING),
                        "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "is_available": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "composition": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "ingredient": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "category": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                    },
                                ),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "measurement_unit": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    enum=["g", "ml", "l", "kg"],
                                ),
                                "minimal_limit": openapi.Schema(
                                    type=openapi.TYPE_NUMBER
                                ),
                                "date_of_arrival": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="date"
                                ),
                            },
                        ),
                        "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Create item",
        operation_description="Use this method to create an item. Only admins can create items",
        request_body=manual_request_schema,
        responses={
            201: openapi.Response("Item created successfully", manual_response_schema)
        },
    )
    def post(self, request):
        """
        Create item method.
        """
        serializer = CreateItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({"id": item.id}, status=201)
        return Response(serializer.errors, status=400)


class ItemListView(generics.ListAPIView):
    """
    List item view. You can filter items by name. Example: /storage/items/?name=Капучино
    """

    queryset = get_items()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ItemFilter

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "is_available": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "composition": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "ingredient": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "category": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                    },
                                ),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "measurement_unit": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    enum=["g", "ml", "l", "kg"],
                                ),
                                "minimal_limit": openapi.Schema(
                                    type=openapi.TYPE_NUMBER
                                ),
                                "date_of_arrival": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="date"
                                ),
                            },
                        ),
                        "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY, items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get items",
        operation_description="Use this method to get all items",
        responses={200: openapi.Response("Items list", list_response_schema)},
    )
    def get(self, request):
        """
        Get items method.
        """
        return super().get(request)


class ItemDetailView(generics.RetrieveAPIView):
    """
    Item detail view.
    """

    queryset = get_items()
    serializer_class = ItemSerializer

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_NUMBER),
            "is_available": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "composition": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "ingredient": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "category": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                        "name": openapi.Schema(
                                            type=openapi.TYPE_STRING
                                        ),
                                    },
                                ),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "measurement_unit": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    enum=["g", "ml", "l", "kg"],
                                ),
                                "minimal_limit": openapi.Schema(
                                    type=openapi.TYPE_NUMBER
                                ),
                                "date_of_arrival": openapi.Schema(
                                    type=openapi.TYPE_STRING, format="date"
                                ),
                            },
                        ),
                        "quantity": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Get specific item",
        operation_description="Use this endpoint to get a specific item",
        responses={200: openapi.Response("Items object", manual_response_schema)},
    )
    def get(self, request, pk=None):
        """
        Get specific item method.
        """
        return super().get(request, pk)


class ItemUpdateView(generics.UpdateAPIView):
    """
    Update item view.
    """

    queryset = get_items()
    serializer_class = UpdateItemSerializer

    @swagger_auto_schema(
        operation_description="Update an Item",
        request_body=UpdateItemSerializer,
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="ID of the item to be updated",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PutImageToItemView(generics.UpdateAPIView):
    """
    Class for putting image to item by item id.
    """

    queryset = get_items()
    serializer_class = PutImageToItemSerializer
    lookup_field = "pk"

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Put image to item",
        operation_description="Use this method to put an image to item",
        request_body=manual_request_schema,
        responses={
            200: openapi.Response("Image added successfully", PutImageToItemSerializer)
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class ItemDestroyView(generics.DestroyAPIView):
    """
    Delete item view.
    """

    queryset = get_items()
    serializer_class = ItemSerializer
    lookup_field = "pk"

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )

    @swagger_auto_schema(
        operation_summary="Delete item",
        operation_description="Use this method to delete an item. Only admins can delete items",
        responses={
            200: openapi.Response("Item deleted successfully", manual_response_schema)
        },
    )
    def delete(self, request, pk):
        """
        Delete item method.
        """
        item = get_items().filter(pk=pk).first()
        item.delete()
        return Response({"message": "Item deleted successfully"}, status=200)


# =====================================================================
# READY MADE PRODUCTS VIEWS
# =====================================================================
class ReadyMadeProductCreateView(generics.CreateAPIView):
    """
    Create ready made product view.
    """

    queryset = get_ready_made_products()
    serializer_class = CreateReadyMadeProductSerializer

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product name"
            ),
            "image": openapi.Schema(
                type=openapi.TYPE_FILE, description="Product image"
            ),
            "price": openapi.Schema(
                type=openapi.TYPE_NUMBER, description="Product price"
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product description"
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Category ID"
            ),
            "available_at_branches": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "branch": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Branch ID"
                        ),
                        "quantity": openapi.Schema(
                            type=openapi.TYPE_NUMBER, description="Quantity"
                        ),
                        "minimal_limit": openapi.Schema(
                            type=openapi.TYPE_NUMBER, description="Minimal limit"
                        ),
                    },
                ),
                description="List of branches where the product is available",
            ),
        },
        required=["name", "available_at_branches"],
    )

    @swagger_auto_schema(request_body=manual_request_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ReadyMadeProductUpdateView(generics.UpdateAPIView):
    """
    Update ready made product view.
    """

    queryset = get_ready_made_products()
    serializer_class = CreateReadyMadeProductSerializer
    lookup_field = "pk"


class ReadyMadeProductListView(generics.ListAPIView):
    """
    List ready made product view. You can filter ready made products by name. Example: /storage/ready-made-products/?name=Круассан
    """

    queryset = get_ready_made_products()
    serializer_class = ReadyMadeProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReadyMadeProductFilter


class ReadyMadeProductDestroyView(generics.DestroyAPIView):
    """
    Delete ready made product view.
    """

    queryset = get_ready_made_products()
    serializer_class = ReadyMadeProductSerializer
    lookup_field = "pk"


class ReadyMadeProductUpdateView(generics.UpdateAPIView):
    """
    Update ready made product view.
    """

    queryset = get_ready_made_products()
    serializer_class = UpdateReadyMadeProductSerializer
    lookup_field = "pk"


class ReadyMadeProductDetailView(generics.RetrieveAPIView):
    """
    Ready made product detail view.
    """

    queryset = get_ready_made_products()
    serializer_class = ReadyMadeProductSerializer
    lookup_field = "pk"


class ReadyMadeProductQuantityUpdateView(generics.UpdateAPIView):
    """
    Class for updating ready made product quantity.
    """

    queryset = get_ready_made_products()
    serializer_class = ReadyMadeProductAvailableAtTheBranchSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"


class PutImageToReadyMadeProductView(generics.UpdateAPIView):
    """
    Class for putting image to ready made product by item id.
    """

    queryset = get_ready_made_products()
    serializer_class = PutImageToReadyMadeProductSerializer
    lookup_field = "pk"

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image": openapi.Schema(type=openapi.TYPE_FILE),
        },
    )

    @swagger_auto_schema(
        operation_summary="Put image to ready made product",
        operation_description="Use this method to put an image to ready made product",
        request_body=manual_request_schema,
        responses={
            200: openapi.Response(
                "Image added successfully", PutImageToReadyMadeProductSerializer
            )
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
