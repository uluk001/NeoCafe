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
