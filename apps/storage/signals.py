from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.storage.models import (
    Item,
    Ingredient,
    Composition,
    AvailableAtTheBranch,
    ReadyMadeProduct,
    ReadyMadeProductAvailableAtTheBranch,
    MinimalLimitReached,
)
from apps.storage.tasks import index_menu_task


models_to_listen = [
    Item,
    Ingredient,
    Composition,
    AvailableAtTheBranch,
    ReadyMadeProduct,
    ReadyMadeProductAvailableAtTheBranch,
    MinimalLimitReached,
]

for model in models_to_listen:

    @receiver(post_save, sender=model)
    def update_algolia(sender, instance, **kwargs):
        """
        Update Algolia index after saving an object.
        """
        index_menu_task.delay()


for model in models_to_listen:

    @receiver(post_delete, sender=model)
    def update_algolia(sender, instance, **kwargs):
        """
        Update Algolia index after deleting an object.
        """
        index_menu_task.delay()
