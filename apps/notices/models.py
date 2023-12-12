from django.db import models
from apps.branches.models import Branch
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
import time
from asgiref.sync import async_to_sync

class BaristaNotification(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=BaristaNotification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        time.sleep(1)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'branch_{instance.branch_id}',
            {
                'type': 'get_notification',
            }
        )

@receiver(post_delete, sender=BaristaNotification)
def send_notification(sender, instance, **kwargs):
    time.sleep(0.5)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'branch_{instance.branch_id}',
        {
            'type': 'get_notification',
        }
    )