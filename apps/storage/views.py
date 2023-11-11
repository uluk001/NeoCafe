from apps.storage.models import AvailableAtTheBranch, Category, Composition, Ingredient, Item
from apps.storage.serializers import CategorySerializer, CompositionSerializer, IngredientSerializer, ItemSerializer, ItemsWithBranchesAndQuantitiesSerializer, EmployeeSerializer, EmployeeUpdateSerializer, ScheduleUpdateSerializer, EmployeeCreateSerializer
from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.storage.services import get_employees


# Categories views
class CreateCategoryView(generics.CreateAPIView):

    @swagger_auto_schema(
        operation_summary="Create category",
        operation_description="Use this method to create a category",
        request_body=CategorySerializer,
        responses={201: openapi.Response('Category created successfully', CategorySerializer)}
    )
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully'}, status=201)
        return Response(serializer.errors, status=400)

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class DestroyCategoryView(generics.DestroyAPIView):
    
    @swagger_auto_schema(
        operation_summary="Delete category",
        operation_description="Use this method to delete a category",
        responses={200: openapi.Response('Category deleted successfully')}
    )
    
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=200)

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ListCategoryView(generics.ListAPIView):

    @swagger_auto_schema(
        operation_summary="Get categories",
        operation_description="Use this method to get all categories",
        responses={200: openapi.Response('Categories list', CategorySerializer(many=True))}
    )
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# Items views
class CreateItemView(APIView):

    @swagger_auto_schema(
        operation_summary="Create item",
        operation_description="Use this method to create an item",
        request_body=ItemSerializer,
        responses={201: openapi.Response('Item created successfully', ItemSerializer)}
    )
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Item created successfully'}, status=201)
        return Response(serializer.errors, status=400)

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Item created successfully'}, status=201)
        return Response(serializer.errors, status=400)


class DestroyItemView(generics.DestroyAPIView):

    @swagger_auto_schema(
        operation_summary="Delete item",
        operation_description="Use this method to delete an item",
        responses={200: openapi.Response('Item deleted successfully')}
    )

    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=200)

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAdminUser]


class ListItemView(generics.ListAPIView):

    @swagger_auto_schema(
        operation_summary="Get items",
        operation_description="Use this method to get all items",
        responses={200: openapi.Response('Items list', ItemSerializer(many=True))}
    )

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAdminUser]


class ItemsWithBranchesAndQuantitiesView(APIView):

    @swagger_auto_schema(
        operation_summary="Get items with branches and quantities",
        operation_description="Use this method to get all items with branches and quantities",
        responses={200: openapi.Response('Items list with branches and quantities', ItemsWithBranchesAndQuantitiesSerializer(many=True))}
    )

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemsWithBranchesAndQuantitiesSerializer(items, many=True)
        return Response(serializer.data)


# Ingredients views
class CreateIngredientView(generics.CreateAPIView):

    @swagger_auto_schema(
        operation_summary="Create ingredient",
        operation_description="Use this method to create an ingredient",
        request_body=IngredientSerializer,
        responses={201: openapi.Response('Ingredient created successfully', IngredientSerializer)}
    )

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ingredient created successfully'}, status=201)
        return Response(serializer.errors, status=400)

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAdminUser]


class DestroyIngredientView(generics.DestroyAPIView):

    @swagger_auto_schema(
        operation_summary="Delete ingredient",
        operation_description="Use this method to delete an ingredient",
        responses={200: openapi.Response('Ingredient deleted successfully')}
    )

    def delete(self, request, pk):
        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.delete()
        return Response({'message': 'Ingredient deleted successfully'}, status=200)

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAdminUser]


class ListIngredientView(generics.ListAPIView):

    @swagger_auto_schema(
        operation_summary="Get ingredients",
        operation_description="Use this method to get all ingredients",
        responses={200: openapi.Response('Ingredients list', IngredientSerializer(many=True))}
    )

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAdminUser]


# Employees views
class CreateEmployeeView(generics.CreateAPIView):

    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Create employee",
        operation_description="Use this method to create an employee",
        request_body=EmployeeCreateSerializer,
        responses={201: openapi.Response('Employee created successfully', EmployeeCreateSerializer)}
    )

    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee created successfully'}, status=201)
        return Response(serializer.errors, status=400)


class EmployeeListView(generics.ListAPIView):

    queryset = get_employees()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'position': openapi.Schema(type=openapi.TYPE_STRING),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'branch': openapi.Schema(type=openapi.TYPE_INTEGER),
            'schedule': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'workdays': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'workday': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'start_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                                'end_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                            }
                        )
                    ),
                }
            ),
        }
    )

    list_response_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=manual_response_schema
    )

    @swagger_auto_schema(
        operation_summary="Get employees",
        operation_description="Use this method to get all employees",
        responses={200: openapi.Response('Employees list', list_response_schema)}
    )
    def get(self, request):
        return super().get(request)      


class EmployeeDetailView(generics.RetrieveAPIView):

    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = get_employees()

    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'position': openapi.Schema(type=openapi.TYPE_STRING),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'branch': openapi.Schema(type=openapi.TYPE_INTEGER),
            'schedule': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'workdays': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'workday': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'start_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                                'end_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                            }
                        )
                    ),
                }
            ),
        }
    )

    @swagger_auto_schema(
        operation_summary="Get specific employee",
        operation_description="Use this endpoint to get a specific employee",
        responses={200: openapi.Response('Employees object', manual_response_schema)}
    )
    def get(self, request, pk=None):
        return super().get(request, pk)


class EmployeeUpdateView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = EmployeeUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'position': openapi.Schema(type=openapi.TYPE_STRING),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'branch': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    )

    @swagger_auto_schema(
        operation_summary="Update employee",
        operation_description="Use this method to update an employee",
        request_body=manual_request_schema,
        responses={200: openapi.Response('Employee updated successfully', EmployeeUpdateSerializer)}
    )

    def put(self, request, pk):
        employee = CustomUser.objects.get(pk=pk)
        serializer = EmployeeUpdateSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee updated successfully'}, status=200)
        return Response(serializer.errors, status=400)


class ScheduleUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ScheduleUpdateSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.kwargs['pk']
        return context