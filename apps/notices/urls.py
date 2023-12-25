from django.urls import path
from .views import (
    ClearWaiterNotificationsView, DeleteBaristaNotificationView,
    DeleteClientNotificationView,
)


urlpatterns = [
    path('delete-barista-notification/', DeleteBaristaNotificationView.as_view()),
    path('delete-client-notification/', DeleteClientNotificationView.as_view()),
    path('clear-waiter-notifications/', ClearWaiterNotificationsView.as_view()),
]
