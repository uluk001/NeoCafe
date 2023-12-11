"""
Module for ordering serializers.
"""
from .services import create_order
from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    """
    Serializer for OrderItem model.
    """
    is_ready_made_product = serializers.BooleanField(read_only=True)
    item_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class OrderSerializer(serializers.Serializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True, required=False)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    spent_bonus_points = serializers.IntegerField(required=True)
    in_an_institution = serializers.BooleanField(required=True)

    def create(self, validated_data):
        return create_order(
            user_id=self.context['request'].user.id,
            total_price=validated_data['total_price'],
            items=validated_data['items'],
            spent_bonus_points=validated_data['spent_bonus_points'],
            in_an_institution=validated_data['in_an_institution'],
        )