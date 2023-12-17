from django.db import transaction
from django.db.models import Prefetch, Sum, Count

from django.forms.models import model_to_dict
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
            item_dict = model_to_dict(item)
            item_dict['is_ready_made_product'] = False
            item_dict['category'] = item.category
            available_items.append(item_dict)

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
            "image": product.image if product.image else None,
            "compositions": [],
            "is_available": True,
            "is_ready_made_product": True,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "image": product.category.image.url if product.category.image else None,
            }
        })

    return ready_made_products


def check_if_ready_made_product_can_be_made(ready_made_product, branch_id, quantity):
    """
    Checks if a ready made product can be made.
    """
    return ReadyMadeProductAvailableAtTheBranch.objects.filter(
        ready_made_product=ready_made_product,
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
        available_items = [item for item in available_items if item['category'].id == int(category_id)]
        available_ready_made_products = [product for product in available_ready_made_products if product['category']['id'] == int(category_id)]

    combined_list = available_items + available_ready_made_products

    return combined_list


def get_popular_items(branch_id):
    item_sales = OrderItem.objects.values('item_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
    product_sales = OrderItem.objects.values('ready_made_product_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    best_selling_items = [(item['item_id'], item['total_quantity']) for item in item_sales]
    best_selling_products = [(product['ready_made_product_id'], product['total_quantity']) for product in product_sales]

    available_items = []
    for item_id, total_quantity in best_selling_items:
        if check_if_items_can_be_made(item_id, branch_id, 1):
            available_items.append((item_id, total_quantity))
            if len(available_items) >= 3:
                break

    available_products = []
    for product_id, total_quantity in best_selling_products:
        if check_if_ready_made_product_can_be_made(product_id, branch_id, 1):
            available_products.append((product_id, total_quantity))
            if len(available_products) >= 3:
                break

    # Объединяем списки и сортируем по общему количеству продаж
    all_available = sorted(available_items + available_products, key=lambda x: x[1], reverse=True)

    # Возвращаем только первые три элемента
    top_selling_available = all_available[:4]

    # Получаем объекты Item и ReadyMadeProduct для возвращаемых ID
    top_selling_available_items = Item.objects.filter(id__in=[item[0] for item in top_selling_available if item in available_items])
    top_selling_available_products = ReadyMadeProduct.objects.filter(id__in=[item[0] for item in top_selling_available if item in available_products])

    return list(top_selling_available_items) + list(top_selling_available_products)


def get_complementary_objects(model, exclude_field, item_id, order_ids):
    return model.objects.filter(
        order__id__in=order_ids
    ).exclude(
        **{exclude_field: item_id}
    ).values(
        exclude_field
    ).annotate(
        count=Count(exclude_field)
    ).order_by('-count')[:3]


def get_compatibles(item_id, is_ready_made_product=False):
    """
    Function to get items that are often ordered with the given item.
    """
    order_ids = OrderItem.objects.filter(
        **{'item_id' if not is_ready_made_product else 'ready_made_product_id': item_id}
    ).values_list('order_id', flat=True)

    complementary_items = get_complementary_objects(OrderItem, 'item_id', item_id, order_ids)
    complementary_ready_made_products = get_complementary_objects(OrderItem, 'ready_made_product_id', item_id, order_ids)

    complementary_items_ids = [item['item_id'] for item in complementary_items]
    complementary_ready_made_products_ids = [product['ready_made_product_id'] for product in complementary_ready_made_products]

    complementary_items = Item.objects.filter(id__in=complementary_items_ids)
    complementary_ready_made_products = ReadyMadeProduct.objects.filter(id__in=complementary_ready_made_products_ids)

    if_items_can_be_made = [item for item in complementary_items if check_if_items_can_be_made(item.id, 1, 1)]
    if_ready_made_products_can_be_made = [product for product in complementary_ready_made_products if check_if_ready_made_product_can_be_made(product.id, 1, 1)]

    return if_items_can_be_made + if_ready_made_products_can_be_made


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


def update_ready_made_product_stock_on_cooking(ready_made_product, branch_id, quantity):
    """
    Updates ready made product stock on cooking.
    """
    try:
        with transaction.atomic():
            available_product = ReadyMadeProductAvailableAtTheBranch.objects.get(
                branch_id=branch_id,
                ready_made_product=ready_made_product
            )
            available_product.quantity -= quantity
            available_product.save()
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