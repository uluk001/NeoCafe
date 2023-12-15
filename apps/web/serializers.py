from rest_framework import serializers
from apps.ordering.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='item.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    clientNumber = serializers.CharField(source='customer.phone_number')
    number = serializers.IntegerField(source='id')

    class Meta:
        model = Order
        fields = ['number', 'clientNumber', 'items', 'status']
