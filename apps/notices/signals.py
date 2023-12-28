from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import time
from apps.notices.models import BaristaNotification, ClentNotification
from apps.storage.models import (
    AvailableAtTheBranch,
    MinimalLimitReached,
    ReadyMadeProductAvailableAtTheBranch,
)
from apps.notices.tasks import (
    update_notifications_on_barista_side,
    update_notifications_on_client_side,
    create_notification_for_admin_task,
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


# Admin notifications
@receiver(post_save, sender=AvailableAtTheBranch)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()


@receiver(post_delete, sender=AvailableAtTheBranch)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()


@receiver(post_save, sender=MinimalLimitReached)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()


@receiver(post_delete, sender=MinimalLimitReached)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()


@receiver(post_save, sender=ReadyMadeProductAvailableAtTheBranch)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()


@receiver(post_delete, sender=ReadyMadeProductAvailableAtTheBranch)
def send_notification(sender, instance, **kwargs):
    create_notification_for_admin_task.delay()
