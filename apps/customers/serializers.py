"""
Module for menu serializers
"""
from rest_framework import serializers
from apps.ordering.models import Order, OrderItem
from apps.storage.serializers import ItemSerializer
from apps.customers.services import (
    get_my_opened_orders_data, get_my_closed_orders_data,
)

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


# ==================== Branch Serializers ====================
class ChangeBranchSerializer(serializers.Serializer):
    """
    Serializer for changing branch
    """

    branch_id = serializers.IntegerField()


# ==================== Order Serializers ====================
class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name')
    item_price = serializers.DecimalField(source='item.price', max_digits=5, decimal_places=2)
    item_total_price = serializers.SerializerMethodField()
    item_image = serializers.ImageField(source='item.image')
    item_id = serializers.IntegerField(source='item.id')
    item_category = serializers.CharField(source='item.category.name')

    class Meta:
        model = OrderItem
        fields = ['item_name', 'item_price', 'quantity', 'item_total_price', 'item_image', 'item_id', 'item_category']

    def get_item_total_price(self, obj):
        return obj.item.price * obj.quantity


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

    class Meta:
        model = Order
        fields = ['id', 'branch_name', 'created_at', 'total_price', 'spent_bonus_points']

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")


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