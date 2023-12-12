from .models import BaristaNotification


def delete_notification(id):
    """
    Deletes notification.
    """
    try:
        notification = BaristaNotification.objects.get(id=id)
        notification.delete()
        return True
    except:
        return False


def create_notification_for_barista(order_id, title, body, branch):
    """
    Creates notification for barista.
    """
    BaristaNotification.objects.create(
        order_id=order_id,
        title=title,
        body=body,
        branch=branch,
    )