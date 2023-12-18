"""
Module for defining the urls for the ordering app.
"""
from django.urls import path
from apps.ordering.views import (
    CreateOrderView, ReorderView,
    ReorderInformationView, AddItemToOrderView,
    RemoveOrderItemView,
)

urlpatterns = [
    path('create-order/', CreateOrderView.as_view()),
    path('reorder/', ReorderView.as_view()),
    path('reorder-information/', ReorderInformationView.as_view()),
    path('add-item-to-order/', AddItemToOrderView.as_view()),
    path('remove-order-item/', RemoveOrderItemView.as_view()),
]