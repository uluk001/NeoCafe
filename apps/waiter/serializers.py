from rest_framework import serializers


class WaiterOpenedOrdersSerializer(serializers.Serializer):
    """
    Serializer for WaiterOpenedOrders model.
    """

    table_number = serializers.IntegerField(required=True)
    order_status = serializers.CharField(required=True)
    order_number = serializers.IntegerField(required=True)
    order_created_at = serializers.DateTimeField(required=True)
