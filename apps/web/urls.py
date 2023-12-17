"""
Module for web app urls
"""
from django.urls import path

from .views import (
    AcceptOrderView, MyBranchIdView,
    CancelOrderView, GetInProcessTakeawayOrdersView,
    GetCanceledTakeawayOrdersView, GetCompletedTakeawayOrdersView,
    GetCanceledInstitutionOrdersView, GetCompletedInstitutionOrdersView,
    GetInProcessInstitutionOrdersView, CompleteOrderView, MakeOrderReadyView,
    GetReadyInstitutionOrdersView, GetReadyTakeawayOrdersView,
)

urlpatterns = [
    # Branch management endpoints
    path("my-branch-id/", MyBranchIdView.as_view()),  # web/my-branch-id/

    # Order management endpoints
    path("accept-order/", AcceptOrderView.as_view()),  # web/accept-order/
    path("complete-order/", CompleteOrderView.as_view()),  # web/complete-order/
    path("cancel-order/", CancelOrderView.as_view()),  # web/cancel-order/
    path("make-order-ready/", MakeOrderReadyView.as_view()),  # web/make-order-ready/

    # Order list endpoints
    path("takeaway-orders/in-process/", GetInProcessTakeawayOrdersView.as_view()),  # web/takeaway-orders/in-process/
    path("takeaway-orders/canceled/", GetCanceledTakeawayOrdersView.as_view()),  # web/takeaway-orders/canceled/
    path("takeaway-orders/ready/", GetReadyTakeawayOrdersView.as_view()),  # web/takeaway-orders/ready/
    path("takeaway-orders/completed/", GetCompletedTakeawayOrdersView.as_view()),  # web/takeaway-orders/completed/
    path("institution-orders/in-process/", GetInProcessInstitutionOrdersView.as_view()),  # web/institution-orders/in-process/
    path("institution-orders/canceled/", GetCanceledInstitutionOrdersView.as_view()),  # web/institution-orders/canceled/
    path("institution-orders/ready/", GetReadyInstitutionOrdersView.as_view()),  # web/institution-orders/ready/
    path("institution-orders/completed/", GetCompletedInstitutionOrdersView.as_view()),  # web/institution-orders/completed/
]