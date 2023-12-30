from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.ordering.tasks import (
    update_new_orders_list_on_barista_side,
)
from apps.notices.tasks import (
    update_notifications_on_barista_side,
    create_reminder,
)

from apps.ordering.models import Order, OrderItem


@receiver(post_save, sender=Order)
def send_notification(sender, instance, **kwargs):
    """
    Sends notification to barista when new order is updated or created.
    """
    update_new_orders_list_on_barista_side.delay(instance.branch_id)
    update_notifications_on_barista_side.delay(instance.branch_id)
    create_reminder.apply_async((instance.branch_id, instance.id), countdown=120)


@receiver(post_delete, sender=Order)
def send_notification(sender, instance, **kwargs):
    """
    Sends notification to barista when new order is deleted.
    """
    update_new_orders_list_on_barista_side.delay(instance.branch_id)
    update_notifications_on_barista_side.delay(instance.branch_id)
