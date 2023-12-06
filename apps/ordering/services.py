"""
Module for services
"""
from django.db import transaction

from apps.ordering.models import Order, OrderItem
from apps.accounts.models import CustomUser
from utils.menu import (
    check_if_items_can_be_made,
    update_ingredient_stock_on_cooking,
)


def create_order(user_id, spent_bonus_points, total_price, items):
    """
    Creates order.
    """
    with transaction.atomic():
        user = CustomUser.objects.get(id=user_id)
        order = Order.objects.create(
            customer=user,
            total_price=total_price,
        )

        order_items = []
        for item in items:
            if not check_if_items_can_be_made(item_id=item['item'].id, branch_id=user.branch.id, quantity=item['quantity']):
                return None
            order_item = OrderItem(
                order=order,
                item=item['item'],
                quantity=item['quantity'],
            )
            order_items.append(order_item)
            update_ingredient_stock_on_cooking(item_id=item['item'].id, quantity=item['quantity'], branch_id=user.branch.id)

        OrderItem.objects.bulk_create(order_items)
        return order
