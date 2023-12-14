from celery import shared_task
from apps.notices.models import BaristaNotification, ClentNotification
from apps.branches.models import Branch
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

SLEEP_TIME = 2

@shared_task
def create_notification_for_barista(order_id, title, body, branch_id):
    """
    Creates notification for barista.
    """
    branch = Branch.objects.get(id=branch_id)
    BaristaNotification.objects.create(
        order_id=order_id,
        title=title,
        body=body,
        branch=branch,
    )


@shared_task
def create_notification_for_client(client_id, title, body):
    """
    Creates notification for client.
    """
    ClentNotification.objects.create(
        client_id=client_id,
        title=title,
        body=body,
    )


@shared_task
def update_notifications_on_barista_side(branch_id):
    """
    Updates notifications on barista side.
    """
    time.sleep(SLEEP_TIME)
    print('update_notifications_on_barista_side')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'branch_{branch_id}',
        {
            'type': 'get_notification',
        }
    )


@shared_task
def update_notifications_on_client_side(client_id):
    """
    Updates notifications on client side.
    """
    time.sleep(SLEEP_TIME)
    print('update_notifications_on_client_side')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{client_id}',
        {
            'type': 'get_notification',
        }
    )
