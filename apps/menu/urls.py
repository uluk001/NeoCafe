"""
Menu URL Configuration
"""
from django.urls import path
from .views import (
    Menu,
)

urlpatterns = [
    path("menu/", Menu.as_view()),
]
