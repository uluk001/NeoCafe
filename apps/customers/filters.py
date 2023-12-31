from utils.menu import (
    combine_items_and_ready_made_products,
)
from apps.storage.models import Item
from django_filters import rest_framework as filters


class MenuFilter(filters.FilterSet):
    """
    Filter for Menu
    """

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category__id = filters.CharFilter(
        field_name="category__id", lookup_expr="icontains"
    )
    can_be_made = filters.BooleanFilter(method="filter_can_be_made")

    class Meta:
        model = Item
        fields = ["name", "category__id", "can_be_made"]

    def filter_can_be_made(self, queryset, name, value):
        if value:
            return queryset.filter(
                id__in=combine_items_and_ready_made_products(
                    self.request.user.branch.id
                )
            )
        return queryset
