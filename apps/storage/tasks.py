from celery import shared_task
from .algolia_setup import index_menu


@shared_task
def index_menu_task():
    """
    Task to index items.
    """
    index_menu()
    return "Items indexed successfully."