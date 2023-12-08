"""
Module for services
"""
from django.db import transaction

from apps.ordering.models import Order, OrderItem
from apps.accounts.models import CustomUser
from apps.storage.algolia_setup import index_items
from utils.menu import (
    check_if_items_can_be_made,
    update_ingredient_stock_on_cooking,
)


def create_order(user_id, spent_bonus_points, total_price, items, in_an_institution):
    """
    Creates order.
    """
    with transaction.atomic():
        user = CustomUser.objects.get(id=user_id)
        order = Order.objects.create(
            customer=user,
            total_price=total_price,
            spent_bonus_points=spent_bonus_points,
            in_an_institution=in_an_institution,
        )

        order_items = []
        if len(items) == 0:
            return None
        for item in items:
            if not check_if_items_can_be_made(item_id=item['item'].id, branch_id=user.branch.id, quantity=item['quantity']):
                index_items()
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
