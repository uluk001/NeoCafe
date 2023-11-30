from apps.accounts.models import CustomUser, EmployeeSchedule
from django.db.models import F

from .models import (
    AvailableAtTheBranch,
    Category,
    Ingredient,
    Item,
    ReadyMadeProduct,
)
from .serializers import (
    IngredientSerializer,
    AvailableAtTheBranchSerializer,
)


def get_employees():
    """Get all employees except clients"""
    employees = CustomUser.objects.exclude(position="client").filter(is_active=True)
    return employees


def get_specific_employee(pk):
    """Get specific employee"""
    employee = CustomUser.objects.filter(pk=pk).first()
    return employee


def get_specific_category(pk):
    """Get specific category"""
    category = Category.objects.filter(pk=pk).first()
    return category


def get_categories():
    """Get all categories"""
    categories = Category.objects.all()
    return categories


def get_ingrediants():
    """Get all ingrediants"""
    ingrediants = Ingredient.objects.all()
    return ingrediants


def get_available_at_the_branch():
    """Get all available at the branch"""
    available_at_the_branch = AvailableAtTheBranch.objects.all()
    return available_at_the_branch


def get_items():
    """Get all items"""
    items = Item.objects.all()
    return items


def get_ready_made_products():
    """Get all ready made products"""
    ready_made_products = ReadyMadeProduct.objects.all()
    return ready_made_products


def delete_employee_schedule_by_employee(employee):
    """Delete employee schedule by employee"""
    title = f"{employee.first_name}'s schedule"
    try:
        employee_schedule = EmployeeSchedule.objects.filter(title=title).first()
        employee_schedule.delete()
        return employee_schedule
    except AttributeError:
        return None


def convert_measurement_unit(value, from_unit, to_unit):
    """Convert measurement unit"""
    conversion_factors = {
        ("g", "kg"): 0.001,
        ("ml", "l"): 0.001,
        ("kg", "g"): 1000,
        ("l", "ml"): 1000,
    }

    conversion_factor = conversion_factors.get((from_unit, to_unit))
    if conversion_factor is not None:
        return value * conversion_factor
    else:
        return value


def get_a_list_of_ingredients_and_their_quantities_in_specific_branch(branch_id):
    """Get a list of ingredients and their quantities in specific branch"""
    available_at_the_branch = AvailableAtTheBranch.objects.filter(branch_id=branch_id).select_related("ingredient")
    serializer = AvailableAtTheBranchSerializer(available_at_the_branch, many=True)
    return serializer.data


def get_low_stock_ingredients_in_branch(branch_id):
    """Get low stock ingredients in branch"""
    low_stock_ingredients = AvailableAtTheBranch.objects.filter(
        branch_id=branch_id,
        quantity__lt=F('ingredient__minimal_limit')
    ).select_related('ingredient').distinct()
    
    serializer = AvailableAtTheBranchSerializer(low_stock_ingredients, many=True)
    return serializer.data
