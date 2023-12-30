from celery import shared_task
from apps.notices.models import (
    BaristaNotification,
    ClentNotification,
    AdminNotification,
    Reminder,
)
from apps.ordering.models import Order
from apps.branches.models import Branch
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from apps.storage.services import (
    get_ingredients_in_stock_more_than_minimal_limit_in_branches,
    get_ready_made_products_in_stock_more_than_minimal_limit_in_branches,
)
from apps.notices.services import (
    if_exists_admin_notification,
    create_admin_notification,
)


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


def create_notification_for_admin(title, running_out_of, branch_id):
    """
    Creates notification for admin.
    """
    branch = Branch.objects.get(id=branch_id)
    AdminNotification.objects.create(
        title=title,
        running_out_of=running_out_of,
        branch=branch,
    )


@shared_task
def update_notifications_on_barista_side(branch_id):
    """
    Updates notifications on barista side.
    """
    time.sleep(SLEEP_TIME)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"branch_{branch_id}",
        {
            "type": "get_notification",
        },
    )


@shared_task
def update_notifications_on_client_side(client_id):
    """
    Updates notifications on client side.
    """
    time.sleep(SLEEP_TIME)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{client_id}",
        {
            "type": "get_notification",
        },
    )


@shared_task
def create_notification_for_admin_task():
    """
    Creates notification for admin.
    """
    ingredients_in_stock_more_than_minimal_limit = (
        get_ingredients_in_stock_more_than_minimal_limit_in_branches()
    )
    ready_made_products_in_stock_more_than_minimal_limit = (
        get_ready_made_products_in_stock_more_than_minimal_limit_in_branches()
    )
    for ingredient in ingredients_in_stock_more_than_minimal_limit:
        if not if_exists_admin_notification(
            f'Ингредиент {ingredient["ingredient_name"]} в филиале {ingredient["name_of_shop"]} заканчивается',
            ingredient["branch_id_annotation"],
        ):
            create_admin_notification(
                f'Ингредиент {ingredient["ingredient_name"]} в филиале {ingredient["name_of_shop"]} заканчивается',
                ingredient["branch_id_annotation"],
            )
    for ready_made_product in ready_made_products_in_stock_more_than_minimal_limit:
        if not if_exists_admin_notification(
            f'Готовый продукт {ready_made_product["ready_made_product_name"]} в филиале {ready_made_product["name_of_shop"]} заканчивается',
            ready_made_product["branch_id_annotation"],
        ):
            create_admin_notification(
                f'Готовый продукт {ready_made_product["ready_made_product_name"]} в филиале {ready_made_product["name_of_shop"]} заканчивается',
                ready_made_product["branch_id_annotation"],
            )
    time.sleep(SLEEP_TIME)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"admin",
        {
            "type": "get_admin_notification",
        },
    )


@shared_task
def create_reminder(branch_id, order_id):
    """
    Creates reminder.
    """
    if Order.objects.filter(id=order_id, status="new").exists():
        branch = Branch.objects.get(id=branch_id)
        Reminder.objects.create(
            content=f"Примите заказ №{order_id}",
            branch=branch,
        )
        time.sleep(SLEEP_TIME)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"reminder_{branch_id}",
            {
                "type": "get_reminder",
            },
        )
