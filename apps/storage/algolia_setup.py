from algoliasearch.search_client import SearchClient
from apps.storage.models import Item, ReadyMadeProduct
from apps.branches.models import Branch
from django.conf import settings
from utils.menu import check_if_items_can_be_made, check_if_ready_made_product_can_be_made


client = SearchClient.create(settings.ALGOLIA_APPLICATION_ID, settings.ALGOLIA_API_KEY)
index = client.init_index('menu')

index.set_settings({
  'attributesForFaceting': ['branch_id']
})


def index_menu():
    """
    Indexes all items in the database
    """
    try:
        branches = Branch.objects.all().only('id')
        items = Item.objects.prefetch_related('compositions__ingredient').all()
        ready_made_product = ReadyMadeProduct.objects.all()

        items_to_index = []
        for branch in branches:
            for item in items:
                if check_if_items_can_be_made(item.id, branch.id, 1):
                    item_to_index = {
                        'objectID': f'{item.id}_{branch.id}',
                        'id': item.id,
                        'name': item.name,
                        'price': float(item.price),
                        'image': item.image.url if item.image else None,
                        'category_name': item.category.name,
                        'description': item.description,
                        'branch_id': branch.id,
                        'ingredients': [{'name': ingredient.name} for ingredient in item.compositions.all()],
                        'is_ready_made_product': False,
                    }
                    items_to_index.append(item_to_index)

            for product in ready_made_product:
                if check_if_ready_made_product_can_be_made(product.id, branch.id, 1):
                    item_to_index = {
                        'objectID': f'{product.id}_{branch.id}',
                        'id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'image': product.image.url if product.image else None,
                        'category_name': product.category.name,
                        'description': product.description,
                        'branch_id': branch.id,
                        'ingredients': [],
                        'is_ready_made_product': True,
                    }
                    items_to_index.append(item_to_index)

        index.save_objects(items_to_index)
    except Exception as e:
        print(e)