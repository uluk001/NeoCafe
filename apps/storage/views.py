from apps.storage.models import AvailableAtTheBranch, Category, Composition, Ingredient, Item, ReadyMadeProduct, ReadyMadeProductAvailableAtTheBranch
from apps.storage.serializers import AvailableAtTheBranchSerializer, CategorySerializer, CompositionSerializer, IngredientSerializer, ItemSerializer, ReadyMadeProductSerializer, ReadyMadeProductAvailableAtTheBranchSerializer, ItemsWithBranchesAndQuantitiesSerializer, EmployeeSerializer
from apps.accounts.models import CustomUser
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @swagger_auto_schema(
        operation_summary="Create employee",
        operation_description="Use this method to create an employee",
        request_body=EmployeeSerializer,
        responses={201: openapi.Response('Employee created successfully', EmployeeSerializer)}
    )

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee created successfully'}, status=201)
        return Response(serializer.errors, status=400)