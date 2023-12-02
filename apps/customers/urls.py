"""
Customers URL Configuration
"""
from django.urls import path

from .views import (BranchesView, ChangeBranchView, CompatibleItemsView, Menu,
                    PopularItemsView)
from apps.storage.views import ItemDetailView

urlpatterns = [
    path("", Menu.as_view()),  # customers/
    path("change-branch/", ChangeBranchView.as_view()),  # customers/change-branch/
    path("branches/", BranchesView.as_view()),  # customers/branches/
    path("popular-items/", PopularItemsView.as_view()),  # customers/popular-items/
    path(
        "compatible-items/<int:item_id>/",
        CompatibleItemsView.as_view(),
    ),  # customers/compatible-items/<item_id>/
    path(
        "<int:pk>/",
        ItemDetailView.as_view(),
    ),  # customers/items/<item_id>/
]
