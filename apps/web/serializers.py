from rest_framework import serializers
from apps.ordering.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'quantity']

    def get_name(self, obj):
        return obj.item.name if obj.ready_made_product is None else obj.ready_made_product.name


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    clientNumber = serializers.CharField(source='customer.phone_number')
    number = serializers.IntegerField(source='id')

    class Meta:
        model = Order
        fields = ['id', 'number', 'clientNumber', 'items', 'status']
