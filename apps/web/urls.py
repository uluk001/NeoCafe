"""
Module for web app urls
"""
from django.urls import path

from .views import (
    AcceptOrderView, MyBranchIdView,

)

urlpatterns = [
    path("accept-order/", AcceptOrderView.as_view()),  # web/accept-order/
    path("my-branch-id/", MyBranchIdView.as_view()),  # web/my-branch-id/
]