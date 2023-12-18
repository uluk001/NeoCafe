from celery import shared_task
from decimal import Decimal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.accounts.models import CustomUser
import time


@shared_task
def update_user_bonus_points(user_id, total_price, spent_bonus_points):
    """
    Updates user bonus points.
    """
    user = CustomUser.objects.get(id=user_id)
    new_bonus_points = Decimal(total_price) * Decimal('0.05')
    user.bonus += new_bonus_points - spent_bonus_points
    user.save()


@shared_task
def update_new_orders_list_on_barista_side(branch_id):
    """
    Updates new orders list on barista side.
    """
    time.sleep(2)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'new_orders_takeaway_{branch_id}',
        {
            'type': 'get_new_orders',
        }
    )
    async_to_sync(channel_layer.group_send)(
        f'new_orders_institution_{branch_id}',
        {
            'type': 'get_new_orders',
        }
    )
