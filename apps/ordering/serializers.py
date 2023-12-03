"""
Module for ordering serializers.
"""
from rest_framework import serializers
from apps.ordering.models import Order, OrderItem
from apps.accounts.models import CustomUser
from apps.storage.models import Item


class TestSerializer(serializers.Serializer):
    """
    Serializer for testing.
    """
    id = serializers.IntegerField()
    branch_id = serializers.IntegerField()
    quantity = serializers.IntegerField()