from django.urls import re_path
from .consumers import NewOrdersTakeawayConsumer

websocket_urlpatterns = [
    re_path(r'ws/new-orders-takeaway/(?P<branch_id>\w+)/$', NewOrdersTakeawayConsumer.as_asgi()),
]