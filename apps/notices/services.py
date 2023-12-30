from .models import (
    BaristaNotification,
    ClentNotification,
    AdminNotification,
    Reminder,
)
from apps.branches.models import Branch
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def delete_baristas_notification(id):
    """
    Deletes notification.
    """
    try:
        notification = BaristaNotification.objects.get(id=id)
        notification.delete()
        return True
    except:
        return False


def delete_client_notification(id):
    """
    Deletes notification.
    """
    try:
        notification = ClentNotification.objects.get(id=id)
        notification.delete()
        return True
    except:
        return False


def clear_waiter_notifications(waiter_id):
    """
    Deletes notifications.
    """
    try:
        notifications = ClentNotification.objects.filter(client_id=waiter_id)
        notifications.delete()
        return True
    except Exception as e:
        return False


def if_exists_admin_notification(text, branch_id):
    """
    Checks if notification exists.
    """
    try:
        branch = Branch.objects.get(id=branch_id)
        notification = AdminNotification.objects.get(text=text, branch=branch)
        return True
    except:
        return False


def create_admin_notification(text, branch_id):
    """
    Creates notification.
    """
    try:
        branch = Branch.objects.get(id=branch_id)
        notification = AdminNotification.objects.create(
            text=text, branch=branch, title="Running out of"
        )
        return True
    except Exception as e:
        print(e)
        return False


def delete_admin_notification(id):
    """
    Deletes admin notification.
    """
    try:
        notification = AdminNotification.objects.get(id=id)
        notification.delete()
        return True
    except:
        return False


def clear_admin_notifications():
    """
    Deletes admin notifications.
    """
    try:
        notifications = AdminNotification.objects.all()
        notifications.delete()
        return True
    except:
        return False


def delete_reminder(id):
    """
    Deletes reminder.
    """
    try:
        notification = Reminder.objects.get(id=id)
        notification.delete()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"reminder_{notification.branch.id}",
            {
                "type": "get_reminder",
            },
        )
        return True
    except:
        return False