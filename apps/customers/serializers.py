"""
Module for menu serializers
"""
from rest_framework import serializers

# ==================== Menu Serializers ====================


# ==================== Branch Serializers ====================
class ChangeBranchSerializer(serializers.Serializer):
    """
    Serializer for changing branch
    """
    branch_id = serializers.IntegerField()


class BranchListSerializer(serializers.Serializer):
    """
    Serializer for list of branches
    """
    name_of_shop = serializers.CharField()
    id = serializers.IntegerField()
