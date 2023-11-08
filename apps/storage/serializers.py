from apps.storage.models import AvailableAtTheBranch, Category, Composition, Ingredient, Item, ReadyMadeProduct, ReadyMadeProductAvailableAtTheBranch
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CompositionSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    ingredient = IngredientSerializer()

    class Meta:
        model = Composition
        fields = '__all__'


class ReadyMadeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyMadeProduct
        fields = '__all__'


class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = AvailableAtTheBranch
        fields = '__all__'


class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    ready_made_product = ReadyMadeProductSerializer()

    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = '__all__'


class ItemDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    composition = CompositionSerializer(many=True)
    available_at_the_branch = AvailableAtTheBranchSerializer(many=True)
    ready_made_product_available_at_the_branch = ReadyMadeProductAvailableAtTheBranchSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class ItemsWithBranchesAndQuantitiesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    available_at_the_branch = AvailableAtTheBranchSerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'