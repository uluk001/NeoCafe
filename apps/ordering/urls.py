"""
Module for defining the urls for the ordering app.
"""
from django.urls import path
from apps.ordering.views import (
    CreateOrderView, ReorderView,
    ReorderInformationView,
)

urlpatterns = [
    path('create-order/', CreateOrderView.as_view()),
    path('reorder/', ReorderView.as_view()),
    path('reorder-information/', ReorderInformationView.as_view()),
]