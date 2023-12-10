"""
Module for menu serializers
"""
from rest_framework import serializers
from apps.storage.serializers import ItemSerializer


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
