import random
from django.db import transaction

from apps.branches.models import Branch
from apps.storage.models import (
    AvailableAtTheBranch, Composition,
    Ingredient, Item, ReadyMadeProduct
)


def get_available_ingredients_with_quantity(branch_id):
    """
    Returns list of available ingredients with their quantities at the branch.
    """
    return [
        {"ingredient": item.ingredient, "quantity": item.quantity}
        for item in AvailableAtTheBranch.objects.filter(branch_id=branch_id).select_related("ingredient")
    ]


def get_items_that_can_be_made(branch_id):
    """
    Returns list of items that can be made at the branch.
    """
    available_ingredients = get_available_ingredients_with_quantity(branch_id)
    available_ingredient_ids = [ingredient['ingredient'].id for ingredient in available_ingredients]

    items = Item.objects.prefetch_related('compositions__ingredient').filter(compositions__ingredient__id__in=available_ingredient_ids)

    items_that_can_be_made = []
    for item in items:
        can_be_made = all(
            composition.quantity <= available_ingredients[composition.ingredient.id]['quantity']
            for composition in item.compositions.all()
            if composition.ingredient.id in available_ingredient_ids
        )
        if can_be_made:
            items_that_can_be_made.append(item)

    return items_that_can_be_made


def get_popular_items(branch_id):
    """
    Returns list of popular items at the branch.
    """
    items_that_can_be_made = get_items_that_can_be_made(branch_id)
    return random.sample(items_that_can_be_made, min(len(items_that_can_be_made), 5))


def get_compatibles(item_id, branch_id):
    """
    Returns list of compatible items with the item at the branch.
    """
    items_that_can_be_made = get_items_that_can_be_made(branch_id)
    return random.sample(items_that_can_be_made, min(len(items_that_can_be_made), 5))


def check_if_items_can_be_made(item_id, branch_id, quantity):
    """
    Checks if the item can be made at the branch.
    """
    available_ingredients = get_available_ingredients_with_quantity(branch_id)
    available_ingredient_ids = {ingredient['ingredient'].id: ingredient['quantity'] for ingredient in available_ingredients}
    
    item = Item.objects.prefetch_related('compositions__ingredient').filter(id=item_id).first()
    
    return all(
        composition.quantity * quantity <= available_ingredient_ids.get(composition.ingredient.id, 0)
        for composition in item.compositions.all()
        if composition.ingredient.id in available_ingredient_ids
    )


def get_available_ready_made_products_with_quantity(branch_id):
    """
    Returns list of available ready made products with their quantities at the branch.
    """
    return [
        {"ready_made_product": item.ready_made_product, "quantity": item.quantity}
        for item in AvailableAtTheBranch.objects.filter(branch_id=branch_id).select_related("ready_made_product")
    ]


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
