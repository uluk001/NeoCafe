from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.notices.models import BaristaNotification, ClentNotification
from apps.notices.tasks import (
    update_notifications_on_barista_side,
    update_notifications_on_client_side,
)


# Barista notifications
@receiver(post_save, sender=BaristaNotification)
def send_notification(sender, instance, **kwargs):
    update_notifications_on_barista_side.delay(instance.branch_id)


@receiver(post_delete, sender=BaristaNotification)
def send_notification(sender, instance, **kwargs):
    update_notifications_on_barista_side.delay(instance.branch_id)


# Client notifications
@receiver(post_save, sender=ClentNotification)
def send_notification(sender, instance, **kwargs):
    update_notifications_on_client_side.delay(instance.client_id)


@receiver(post_delete, sender=ClentNotification)
def send_notification(sender, instance, **kwargs):
    update_notifications_on_client_side.delay(instance.client_id)
