from django.urls import path
from apps.waiter.views import (
    GetTableAvailibilityView, TableDetailView,
    WaiterOpenedOrdersView,
)

urlpatterns = [
    path('get-table-availibility/', GetTableAvailibilityView.as_view()),
    path('get-table-detail/', TableDetailView.as_view()),
    path('get-orders-in-institution/', WaiterOpenedOrdersView.as_view()),
]
