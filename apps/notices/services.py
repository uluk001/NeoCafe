from .models import BaristaNotification, ClentNotification


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


def create_notification_for_client(client_id, title, body):
    """
    Creates notification for client.
    """
    ClentNotification.objects.create(
        client_id=client_id,
        title=title,
        body=body,
    )


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
