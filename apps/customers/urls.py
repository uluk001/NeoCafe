"""
Customers URL Configuration
"""
from django.urls import path

from .views import (
    ChangeBranchView, CompatibleItemsView, Menu,
    PopularItemsView, ItemSearchView
)
from apps.storage.views import ItemDetailView, ListCategoryView
from apps.branches.views import BranchListView

urlpatterns = [
    path("menu", Menu.as_view()),  # customers/
    path(
        "menu/<int:pk>/",
        ItemDetailView.as_view(),
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
]
