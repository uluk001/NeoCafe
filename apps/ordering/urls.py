"""
Module for defining the urls for the ordering app.
"""
from django.urls import path
from apps.ordering.views import TestView

urlpatterns = [
    path("test/", TestView.as_view()),
]