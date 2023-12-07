from algoliasearch.search_client import SearchClient
from django.conf import settings
from apps.storage.models import Item, Ingredient, Composition, AvailableAtTheBranch, ReadyMadeProduct
from apps.branches.models import Branch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

client = SearchClient.create(settings.ALGOLIA_APPLICATION_ID, settings.ALGOLIA_API_KEY)
index = client.init_index('items')



def index_items():
    try:
        items = Item.objects.all()
        items_to_index = []
        for item in items:
            item_to_index = {
                'objectID': item.id,
                'name': item.name,
                'price': item.price,
                'description': item.description,
                'category': item.category,
                'is_available': item.is_available,
                'ingredients': [],
            }
            for composition in item.compositions.all():
                ingredient = composition.ingredient
                item_to_index['ingredients'].append({
                    'id': ingredient.id,
                    'name': ingredient.name,
                    'quantity': composition.quantity,
                })
            items_to_index.append(item_to_index)
        index.save_objects(items_to_index)
        return True
    except Exception as e:
        print(e)


@receiver(post_save, sender=Item)
def update_algolia(sender, instance, created, **kwargs):
    """
    Update Algolia index after saving an Item.
    """
    if created:
        index_items()