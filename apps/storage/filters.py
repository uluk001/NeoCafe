"""
Module for filters
"""
from django_filters import rest_framework as filters

from apps.accounts.models import CustomUser
from apps.branches.models import Branch
from apps.storage.models import (
    AvailableAtTheBranch, Category, Composition,
    Ingredient, Item, ReadyMadeProduct
)

from .services import get_employees


class ItemFilter(filters.FilterSet):
    """
    Filter for Item
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category__name = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )

    class Meta:
        model = Item
        fields = ["name", "category__name"]


class IngredientFilter(filters.FilterSet):
    """
    Filter for Ingredient
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["name"]


class ReadyMadeProductFilter(filters.FilterSet):
    """
    Filter for ReadyMadeProduct
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ReadyMadeProduct
        fields = ["name"]


class EmployeeFilter(filters.FilterSet):
    """
    Filter for Employee
    """

    name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    position = filters.CharFilter(field_name="position", lookup_expr="icontains")
    branch = filters.NumberFilter(field_name="branch__id")

    class Meta:
        model = CustomUser
        fields = ["name", "position"]

    def get_queryset(self):
        return get_employees()
