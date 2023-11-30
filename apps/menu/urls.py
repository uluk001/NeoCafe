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
    path("", Menu.as_view()), # menu/
    path("change-branch/", ChangeBranchView.as_view()), # menu/change-branch/
    path("branches/", BranchesView.as_view()), # menu/branches/
]
