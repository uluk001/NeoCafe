from apps.branches.models import Branch
from apps.storage.models import Ingredient, Item, Composition, AvailableAtTheBranch

def get_available_ingredients_with_quantity(branch_id):
    """
    Returns a list of available ingredients with quantity.
    """
    available_ingredients = []
    available_at_the_branch = AvailableAtTheBranch.objects.filter(branch_id=branch_id)
    for item in available_at_the_branch:
        available_ingredients.append(
            {
                "ingredient": item.ingredient,
                "quantity": item.quantity,
            }
        )
    return available_ingredients


def get_items_that_can_be_made(branch_id):
    """
    Returns a list of items that can be made.
    """
    available_ingredients = get_available_ingredients_with_quantity(branch_id)
    items_that_can_be_made = []
    for item in Item.objects.all():
        can_be_made = True
        for composition in item.compositions.all():
            for available_ingredient in available_ingredients:
                if (
                    composition.ingredient == available_ingredient["ingredient"]
                    and composition.quantity > available_ingredient["quantity"]
                ):
                    can_be_made = False
        if can_be_made:
            items_that_can_be_made.append(item)
    return items_that_can_be_made


def get_available_ingredients_with_quantity(branch_id):
    available_at_the_branch = AvailableAtTheBranch.objects.filter(branch_id=branch_id).select_related('ingredient')
    return [{"ingredient": item.ingredient, "quantity": item.quantity} for item in available_at_the_branch]
