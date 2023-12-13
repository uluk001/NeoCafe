from django.urls import path
from .views import *


urlpatterns = [
    path('delete-barista-notification/', DeleteBaristaNotificationView.as_view()),
    path('delete-client-notification/', DeleteClientNotificationView.as_view()),
]
