"""
Customers URL Configuration
"""
from django.urls import path

from .views import (
    ChangeBranchView,
    CompatibleItemsView,
    Menu,
    PopularItemsView,
    ItemSearchView,
    MyBonusesView,
    CheckIfItemCanBeMadeView,
    MyOrdersView,
    MyOrderDetailView,
    MyIdView,
    MenuItemDetailView,
)
from apps.storage.views import (
    ListCategoryView,
)
from apps.branches.views import BranchListView

urlpatterns = [
    path("menu", Menu.as_view()),  # customers/
    path(
        "menu/<int:item_id>/",
        MenuItemDetailView.as_view(),
    ),  # customers/items/<item_id>/
    path(
        "compatible-items/<int:item_id>/",
        CompatibleItemsView.as_view(),
    ),  # customers/compatible-items/<item_id>/
    path("popular-items/", PopularItemsView.as_view()),  # customers/popular-items/
    path("categories/", ListCategoryView.as_view()),  # customers/categories/
    path("change-branch/", ChangeBranchView.as_view()),  # customers/change-branch/
    path("branches/", BranchListView.as_view()),  # customers/branches/
    path("search/", ItemSearchView.as_view()),  # customers/search/
    path("my-bonus/", MyBonusesView.as_view()),  # customers/my-bonus/
    path("my-id/", MyIdView.as_view()),  # customers/my-id/
    path(
        "check-if-item-can-be-made/",
        CheckIfItemCanBeMadeView.as_view(),
    ),  # customers/check-if-item-can-be-made/
    path("my-orders/", MyOrdersView.as_view()),  # customers/my-orders/
    path(
        "my-orders/<int:pk>/",
        MyOrderDetailView.as_view(),
    ),  # customers/my-orders/<order_id>/
]
