"""
Module for services
"""
from django.db import transaction

from apps.ordering.models import Order, OrderItem
from apps.accounts.models import CustomUser
from utils.menu import (
    check_if_items_can_be_made,
    update_ingredient_stock_on_cooking,
    check_if_ready_made_product_can_be_made,
    update_ready_made_product_stock_on_cooking,
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
            branch=user.branch,
        )

        order_items = []
        if len(items) == 0:
            return None
        for item in items:
            if item['ready_made_product']:
                if check_if_ready_made_product_can_be_made(item['ready_made_product'], user.branch, item['quantity']):
                    order_items.append(
                        OrderItem(
                            order=order,
                            ready_made_product=item['ready_made_product'],
                            quantity=item['quantity'],
                        )
                    )
                    update_ready_made_product_stock_on_cooking(item['ready_made_product'], user.branch, item['quantity'])
            else:
                if check_if_items_can_be_made(item['item'], user.branch.id, item['quantity']):
                    order_items.append(
                        OrderItem(
                            order=order,
                            item=item['item'],
                            quantity=item['quantity'],
                        )
                    )
                    update_ingredient_stock_on_cooking(item['item'], user.branch, item['quantity'])
        OrderItem.objects.bulk_create(order_items)
        return order
