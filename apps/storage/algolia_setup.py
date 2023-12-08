from algoliasearch.search_client import SearchClient
from django.conf import settings
from apps.storage.models import Item, Ingredient, Composition, AvailableAtTheBranch, ReadyMadeProduct
from apps.branches.models import Branch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from utils.menu import check_if_items_can_be_made

client = SearchClient.create(settings.ALGOLIA_APPLICATION_ID, settings.ALGOLIA_API_KEY)
index = client.init_index('items')

index.set_settings({
  'attributesForFaceting': ['branch_id']
})

def index_items():
    """
    Indexes all items in the database
    """
    try:
        branches = Branch.objects.all().only('id')
        items = Item.objects.all()
        items_to_index = []
        for branch in branches:
            for i in items:
                if check_if_items_can_be_made(i.id, branch.id, 1):
                    item_to_index = {
                        'objectID': f'{i.id}_{branch.id}',
                        'id': i.id,
                        'name': i.name,
                        'price': float(i.price),
                        'image': i.image.url if i.image else None,
                        'category_name': i.category.name,
                        'description': i.description,
                        'branch_id': branch.id,
                        'ingredients': []
                    }
                    for composition in i.compositions.all():
                        ingredient = Ingredient.objects.get(id=composition.ingredient_id)
                        item_to_index['ingredients'].append({
                            'name': ingredient.name,
                        })
                    items_to_index.append(item_to_index)
        index.save_objects(items_to_index)
        return items_to_index
    except Exception as e:
        print(e)
        return None


@receiver(post_save, sender=Item)
def update_algolia(sender, instance, created, **kwargs):
    """
    Update Algolia index after saving an Item.
    """
    if created:
        index_items()
