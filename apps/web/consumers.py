from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .services import get_orders, get_only_required_fields
from apps.ordering.models import Order, OrderItem


class NewOrdersTakeawayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.branch_id = self.scope['url_route']['kwargs']['branch_id']
        self.branch_group_name = f'branch_{self.branch_id}'
        # Connect to group
        await self.channel_layer.group_add(
            self.branch_group_name,
            self.channel_name
        )

        await self.accept()
        await self.get_new_orders()

    async def disconnect(self, close_code):
        # Disconnect from group
        await self.channel_layer.group_discard(
            self.branch_group_name,
            self.channel_name
        )

    async def get_new_orders(self, event=None):
        orders = await sync_to_async(get_orders)(
            branch_id=self.branch_id,
            in_an_institution=False,
            status='new',
        )

        orders_data = []
        for order in orders:
            order_data = await sync_to_async(get_only_required_fields)(order)
            orders_data.append(order_data)

        await self.send(text_data=json.dumps({
            'orders': orders_data
        }))

    async def get_new_orders_handler(self, event):
        await self.get_new_orders()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # Handle received data if needed

    async def send_order(self, event):
        order = event['order']

        # Send message to barista
        await self.send(text_data=json.dumps({
            'order': order
        }))
