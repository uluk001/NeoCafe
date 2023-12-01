"""
Customers URL Configuration
"""
from django.urls import path
from .views import (
    Menu,
    ChangeBranchView,
    BranchesView,
)

urlpatterns = [
    path("", Menu.as_view()),  # customers/
    path("change-branch/", ChangeBranchView.as_view()),  # customers/change-branch/
    path("branches/", BranchesView.as_view()),  # customers/branches/
]
