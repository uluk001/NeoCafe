from django.urls import re_path
from .consumers import NewOrdersTakeawayConsumer, NewOrdersInstitutionConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/new-orders-takeaway/(?P<branch_id>\w+)/$",
        NewOrdersTakeawayConsumer.as_asgi(),
    ),
    re_path(
        r"ws/new-orders-institution/(?P<branch_id>\w+)/$",
        NewOrdersInstitutionConsumer.as_asgi(),
    ),
]
