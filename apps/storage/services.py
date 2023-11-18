from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays

from .models import (AvailableAtTheBranch, Category, Composition, Ingredient,
                     Item, ReadyMadeProduct)


def get_employees():
    """Get all employees except clients"""
    employees = CustomUser.objects.exclude(position="client").filter(is_active=True)
    return employees


def get_specific_employee(pk):
    """Get specific employee"""
    employee = CustomUser.objects.filter(pk=pk).first()
    return employee
