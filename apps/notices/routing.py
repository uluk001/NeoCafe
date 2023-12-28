from django.urls import re_path
from .consumers import (
    OrderNotificationToBaristaConsumer,
    NotificationToClentConsumer,
    NotificationToAdminConsumer,
)


websocket_urlpatterns = [
    re_path(
        r"ws/to-baristas/branch/(?P<branch_id>\w+)/$",
        OrderNotificationToBaristaConsumer.as_asgi(),
    ),
    re_path(r"ws/to-clients/(?P<user_id>\w+)/$", NotificationToClentConsumer.as_asgi()),
    re_path(r"ws/notifications/admin/$", NotificationToAdminConsumer.as_asgi()),
]
