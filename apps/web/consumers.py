from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .services import get_orders


class NewOrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.branch_id = self.scope['url_route']['kwargs']['branch_id']
        self.branch_group_name = f'branch_{self.branch_id}'
        # Connect to group
        await self.channel_layer.group_add(
            self.branch_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Disconnect from group
        await self.channel_layer.group_discard(
            self.branch_group_name,
            self.channel_name
        )

    async def get_new_orders(self, event):
        await self.send(text_data=json.dumps({
            'orders': await get_orders(self.branch_id)
        }))
