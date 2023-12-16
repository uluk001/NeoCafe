import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import BaristaNotification, ClentNotification
from apps.accounts.models import CustomUser

class OrderNotificationToBaristaConsumer(AsyncWebsocketConsumer):
    """
    Consumer for sending notifications to barista.
    """
    async def connect(self):
        self.branch_id = self.scope['url_route']['kwargs']['branch_id']
        self.branch_group_name = f'branch_{self.branch_id}'
        # Connect to group
        await self.channel_layer.group_add(
            self.branch_group_name,
            self.channel_name
        )

        await self.accept()
        await self.get_notification()

    async def disconnect(self, close_code):
        # Disconnect from group
        await self.channel_layer.group_discard(
            self.branch_group_name,
            self.channel_name
        )

    async def get_notification(self, event=None):
        # Send message to barista
        notifications = await sync_to_async(
            list, thread_sensitive=True
        )(
            BaristaNotification.objects.filter(branch_id=self.branch_id)
        )
        notifications_list = []
        for notification in notifications:
            notifications_list.append({
                'id': notification.id,
                'order_id': notification.order_id,
                'title': notification.title,
                'body': notification.body,
                'exactly_time': notification.created_at.strftime('%H:%M'),
                'created_at': notification.created_at.strftime('%d.%m.%Y')
            })
        await self.send(text_data=json.dumps({
            'notifications': notifications_list
        }))

    async def get_notification_handler(self, event):
        await self.get_notification()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Handle received data if needed

    async def receive_get_notification(self, event):
        await self.get_notification()

    async def send_order_notification(self, event):
        order = event['order']

        # Send message to barista
        await self.send(text_data=json.dumps({
            'order': order
        }))

    async def handle_get_notification(self, event):
        await self.get_notification()


# =============================================================
# Client Notifications
# ============================================================
class NotificationToClentConsumer(AsyncWebsocketConsumer):
    """
    Consumer for sending notifications to client.
    """
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'
        # Connect to group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()
        await self.get_notification()

    async def disconnect(self, close_code):
        # Disconnect from group

        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def get_notification(self, event=None):
        # Send message to barista
        notifications = await sync_to_async(
            list, thread_sensitive=True
        )(
            ClentNotification.objects.filter(client_id=self.user_id)
        )
        notifications_list = []
        for notification in notifications:
            notifications_list.append({
                'id': notification.id,
                'title': notification.title,
                'body': notification.body,
                'exactly_time': notification.created_at.strftime('%H:%M'),
                'created_at': notification.created_at.strftime('%d.%m.%Y')
            })
        await self.send(text_data=json.dumps({
            'notifications': notifications_list
        }))

    async def get_notification_handler(self, event):
        await self.get_notification()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

    async def send_order_notification(self, event):
        order = event['order']

        # Send message to barista
        await self.send(text_data=json.dumps({
            'order': order
        }))

    async def handle_get_notification(self, event):
        await self.get_notification()

    async def receive_get_notification(self, event):
        await self.get_notification()