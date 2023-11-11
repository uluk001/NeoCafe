from .models import Category, Item, Ingredient, Composition, ReadyMadeProduct, AvailableAtTheBranch
from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays


def get_employees():
    """Get all employees except clients"""
    employees = CustomUser.objects.exclude(position='client').filter(is_active=True)
    return employees


def get_specific_employee(pk):
    """Get specific employee"""
    employee = CustomUser.objects.filter(pk=pk).first()
    return employee