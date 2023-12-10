from django.db import transaction
from django.db.models import Prefetch, Sum, Count

from algoliasearch.search_client import SearchClient
from django.conf import settings

from apps.storage.models import (
    AvailableAtTheBranch, Composition,
    Ingredient, Item, ReadyMadeProduct,
    MinimalLimitReached, ReadyMadeProductAvailableAtTheBranch,
)
from apps.ordering.models import OrderItem


client = SearchClient.create(settings.ALGOLIA_APPLICATION_ID, settings.ALGOLIA_API_KEY)
index = client.init_index('items')


def get_available_items(branch_id):
    available_ingredients = AvailableAtTheBranch.objects.filter(branch_id=branch_id)
    ingredient_quantities = {ingredient.ingredient_id: ingredient.quantity for ingredient in available_ingredients}

    compositions_prefetch = Prefetch('compositions', queryset=Composition.objects.all())
    all_items = Item.objects.prefetch_related(compositions_prefetch).all()

    available_items = []
    for item in all_items:
        can_make = True
        for composition in item.compositions.all():
            required_ingredient_id = composition.ingredient_id
            required_quantity = composition.quantity

            if required_ingredient_id not in ingredient_quantities or \
               ingredient_quantities[required_ingredient_id] < required_quantity:
                can_make = False
                break

        if can_make:
            available_items.append(item)

    return available_items


def get_available_ready_made_products(branch_id):
    """
    Returns list of available ready made products at the branch.
    """
    available_ready_made_products = ReadyMadeProduct.objects.filter(
        availables__branch_id=branch_id,
        availables__quantity__gt=0
    )

    ready_made_products = []
    for product in available_ready_made_products:
        ready_made_products.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "image": product.image.url if product.image else None,
            "compositions": [],
            "is_available": True,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "image": product.category.image.url if product.category.image else None,
            }
        })

    return ready_made_products


def check_if_ready_made_product_can_be_made(product_id, branch_id, quantity):
    """
    Checks if a ready made product can be made.
    """
    return ReadyMadeProductAvailableAtTheBranch.objects.filter(
        product_id=product_id,
        branch_id=branch_id,
        quantity__gte=quantity
    ).exists()


def combine_items_and_ready_made_products(branch_id, category_id=None):
    """
    Combines items and ready made products into one list.
    """
    available_items = get_available_items(branch_id)
    available_ready_made_products = get_available_ready_made_products(branch_id)
    if category_id:
        available_items = [item for item in available_items if item.category.id == int(category_id)]
        print(available_items)
        available_ready_made_products = [product for product in available_ready_made_products if product['category']['id'] == int(category_id)]

    combined_list = list(available_items) + available_ready_made_products

    return combined_list


def get_popular_items(branch_id):
    item_sales = OrderItem.objects.values('item_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
    best_selling_item_ids = [item['item_id'] for item in item_sales]

    available_items = []
    for item_id in best_selling_item_ids:
        if check_if_items_can_be_made(item_id, branch_id, 1):
            available_items.append(item_id)
            if len(available_items) >= 3:
                break

    top_selling_available_items = Item.objects.filter(id__in=available_items).order_by('-id')[:3]

    return top_selling_available_items


def get_compatibles(item_id):
    """
    Function to get items that are often ordered with the given item.

    Args:
    item_id (int): The ID of the item for which complementary items are sought.

    Returns:
    list: A list of up to three items most frequently ordered with the given item.
    """
    order_ids = OrderItem.objects.filter(item_id=item_id).values_list('order_id', flat=True)

    complementary_items = OrderItem.objects.filter(
        order__id__in=order_ids
    ).exclude(
        item_id=item_id
    ).values('item_id').annotate(
        count=Count('item_id')
    ).order_by('-count')[:3]

    items = Item.objects.filter(id__in=[item['item_id'] for item in complementary_items])
    return items



def update_ingredient_stock_on_cooking(item_id, branch_id, quantity):
    """
    Updates ingredient stock on cooking.
    """
    try:
        with transaction.atomic():
            compositions = Composition.objects.filter(item_id=item_id).select_related('ingredient')
            ingredients_to_update = []

            for composition in compositions:
                available_ingredient = AvailableAtTheBranch.objects.get(
                    branch_id=branch_id,
                    ingredient_id=composition.ingredient_id
                )
                available_ingredient.quantity -= composition.quantity * quantity
                ingredients_to_update.append(available_ingredient)

            AvailableAtTheBranch.objects.bulk_update(ingredients_to_update, ['quantity'])
            return "Updated successfully."
    except Exception as e:
        raise e


def check_if_items_can_be_made(item_id, branch_id, quantity):
    required_ingredients = Composition.objects.filter(item_id=item_id)

    for ingredient in required_ingredients:
        total_available = AvailableAtTheBranch.objects.filter(
            branch_id=branch_id, 
            ingredient_id=ingredient.ingredient_id
        ).aggregate(
            total=Sum('quantity')
        )['total']
        if total_available is None or total_available < ingredient.quantity * quantity:
            return False

    return True


def item_search(query, branch_id):
    """
    Returns list of items that match the query.
    """
    items = index.search(query, {
        'filters': f'branch_id:{branch_id}'
    })['hits']

    return items