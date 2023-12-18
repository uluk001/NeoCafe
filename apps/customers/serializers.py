"""
Module for menu serializers
"""
from rest_framework import serializers
from apps.ordering.models import Order, OrderItem
from apps.storage.serializers import ItemSerializer, CategorySerializer
from apps.customers.services import (
    get_my_opened_orders_data, get_my_closed_orders_data,
)
import random
from apps.storage.models import Item, ReadyMadeProduct

# ==================== Menu Serializers ====================
class GetCompatibleItemsSerializer(serializers.Serializer):
    """
    Serializer for getting compatible items
    """

    item_id = serializers.IntegerField()


class ExtendedItemSerializer(ItemSerializer):
    is_ready_made_product = serializers.BooleanField()

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['is_ready_made_product']


class CheckIfItemCanBeMadeSerializer(serializers.Serializer):
    """
    Serializer for checking if item can be made
    """

    is_ready_made_product = serializers.BooleanField()
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class MenuItemDetailSerializer(serializers.Serializer):

    ready_made_product_compositions = [
        "Мед с горы Олимп", "Золотые яблоки из садов Гесперид",
        "Рис выращенный на полях", "Остролист, собранный эльфами на рассвете",
        "Пыльца невидимого орхидеи", "Светлячки, пойманные в полночь", "Капля чернил каракатицы",
        "Отражение первой звезды", "Слеза единорога", "Сердце дракона", "Кровь феникса",
    ]

    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    image = serializers.ImageField()
    compositions = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(required=False)
    category = CategorySerializer()

    class Meta:
        fields = ['id', 'name', 'description', 'price', 'image', 'compositions', 'is_available', 'category']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, Item):
            representation['is_ready_made_product'] = False
            representation['is_available'] = instance.is_available
            representation['image'] = instance.image.url
        elif isinstance(instance, ReadyMadeProduct):
            representation['is_ready_made_product'] = True
            representation['is_available'] = True
            representation['image'] = instance.image.url
        return representation

    def get_compositions(self, obj):
        if isinstance(obj, Item):
            compositions = obj.compositions.all()
            compositions_list = []
            for composition in compositions:
                compositions_list.append({
                    'id': composition.id,
                    'name': composition.ingredient.name,
                    'quantity': composition.quantity,
                })
            return compositions_list
        elif isinstance(obj, ReadyMadeProduct):
            random_ingredients = random.sample(self.ready_made_product_compositions, random.randint(1, 5))
            compositions_list = []
            for ingredient in random_ingredients:
                compositions_list.append({
                    'id': random.randint(1, 100),
                    'name': ingredient,
                    'quantity': random.randint(1, 5),
                })
            return compositions_list


# ==================== Branch Serializers ====================
class ChangeBranchSerializer(serializers.Serializer):
    """
    Serializer for changing branch
    """

    branch_id = serializers.IntegerField()


# ==================== Order Serializers ====================
class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()
    item_total_price = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    item_id = serializers.SerializerMetaclass
    item_category = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['item_name', 'item_price', 'quantity', 'item_total_price', 'item_image', 'item_id', 'item_category']

    def get_item_total_price(self, obj):
        if obj.item is not None:
            return obj.item.price * obj.quantity
        return obj.ready_made_product.price * obj.quantity

    def get_item_name(self, obj):
        if obj.item is not None:
            return obj.item.name
        return obj.ready_made_product.name

    def get_item_price(self, obj):
        if obj.item is not None:
            return obj.item.price
        return obj.ready_made_product.price

    def get_item_image(self, obj):
        if obj.item is not None:
            return obj.item.image.url
        return obj.ready_made_product.image.url

    def get_item_id(self, obj):
        if obj.item is not None:
            return obj.item.id
        return obj.ready_made_product.id

    def get_item_category(self, obj):
        if obj.item is not None:
            return obj.item.category.name
        return obj.ready_made_product.category.name


class OrderSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name_of_shop')
    items = OrderItemSerializer(many=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'branch_name', 'created_at', 'items', 'total_price', 'spent_bonus_points']

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")


class MyOrdersListSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name_of_shop')
    created_at = serializers.SerializerMethodField()
    branch__image = serializers.ImageField(source='branch.image')
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'branch_name', 'created_at', 'total_price', 'spent_bonus_points', 'branch__image', 'order_items']

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")

    def get_order_items(self, obj):
        items = ', '.join([item.item.name for item in obj.items.all() if item.item is not None])
        ready_made_products = ', '.join([item.ready_made_product.name for item in obj.items.all() if item.ready_made_product is not None])
        return items + ready_made_products


class UserOrdersSerializer(serializers.Serializer):
    opened_orders = serializers.SerializerMethodField()
    closed_orders = serializers.SerializerMethodField()

    class Meta:
        fields = ['opened_orders', 'closed_orders']

    def get_opened_orders(self, obj):
        orders = get_my_opened_orders_data(obj)
        return MyOrdersListSerializer(orders, many=True).data

    def get_closed_orders(self, obj):
        orders = get_my_closed_orders_data(obj)
        return MyOrdersListSerializer(orders, many=True).data
