from django.urls import path
from .views import (
    ClearWaiterNotificationsView, DeleteBaristaNotificationView,
    DeleteClientNotificationView, ClearAdminNotificationsView,
    DeleteAdminNotificationView,
)


urlpatterns = [
    path('delete-barista-notification/', DeleteBaristaNotificationView.as_view()),
    path('delete-client-notification/', DeleteClientNotificationView.as_view()),
    path('clear-waiter-notifications/', ClearWaiterNotificationsView.as_view()),
    path('clear-admin-notifications/', ClearAdminNotificationsView.as_view()),
    path('delete-admin-notification/', DeleteAdminNotificationView.as_view()),
]
