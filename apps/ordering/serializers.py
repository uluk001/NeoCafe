"""
Module for ordering serializers.
"""
from rest_framework import serializers
from apps.ordering.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity',]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'spent_bonus_points',
            'in_an_institution',
            'items',
            ]
