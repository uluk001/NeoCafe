"""
Menu URL Configuration
"""
from django.urls import path
from .views import (
    Menu,
    ChangeBranchView,
    BranchesView,
)

urlpatterns = [
    path("", Menu.as_view()),
    path("change-branch/", ChangeBranchView.as_view()),
    path("branches/", BranchesView.as_view()),
]
