from django.urls import re_path
from .consumers import OrderNotificationToBaristaConsumer


websocket_urlpatterns = [
    re_path(r'ws/to-baristas/branch/(?P<branch_id>\w+)/$', OrderNotificationToBaristaConsumer.as_asgi()),
]
