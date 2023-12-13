"""
Module for services
"""
from django.db import transaction

from apps.ordering.models import Order, OrderItem
from apps.storage.models import ReadyMadeProduct, Item
from apps.accounts.models import CustomUser
from apps.notices.services import create_notification_for_barista, create_notification_for_client
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
        new_bonus_points = int(total_price * 0.05)
        user.bonus += new_bonus_points - spent_bonus_points
        user.save()

        order_items = []
        if len(items) == 0:
            return None
        for item in items:
            is_ready_made_product = item['is_ready_made_product']
            item_id = item['item_id']
            if is_ready_made_product:
                ready_made_product_instance = ReadyMadeProduct.objects.get(id=item_id)
                if check_if_ready_made_product_can_be_made(ready_made_product_instance, user.branch, item['quantity']):
                    quantity = item['quantity']
                    order_items.append(
                        OrderItem(
                            order=order,
                            ready_made_product=ready_made_product_instance,
                            quantity=quantity,
                        )
                    )
                    update_ready_made_product_stock_on_cooking(ready_made_product_instance, user.branch, item['quantity'])
            else:
                item_instance = Item.objects.get(id=item_id)
                if check_if_items_can_be_made(item_instance, user.branch.id, item['quantity']):
                    quantity = item['quantity']
                    order_items.append(
                        OrderItem(
                            order=order,
                            item=item_instance,
                            quantity=quantity,
                        )
                    )
                    update_ingredient_stock_on_cooking(item_instance, user.branch, item['quantity'])
        OrderItem.objects.bulk_create(order_items)
        order_items_names_and_quantities = get_order_items_names_and_quantities(order_items)
        order_items_names_and_quantities_str = ', '.join(
            [f"{order_item['name']} х{order_item['quantity']}" for order_item in order_items_names_and_quantities]
        )
        create_notification_for_client(
            client_id=user.id,
            title=f'Ваш заказ №{order.id} принят' if in_an_institution else f'Ваш заказ №{order.id} принят',
            body=order_items_names_and_quantities_str,
        )
        create_notification_for_barista(
            order_id=order.id,
            title=f'Ваш заказ оформлен',
            body=order_items_names_and_quantities_str,
        )
        return order


def get_order_items_names_and_quantities(order_items):
    """
    Returns order items names and quantities.
    """
    order_items_names_and_quantities = []
    for order_item in order_items:
        if order_item.ready_made_product:
            order_items_names_and_quantities.append(
                {
                    'name': order_item.ready_made_product.name,
                    'quantity': order_item.quantity,
                }
            )
        else:
            order_items_names_and_quantities.append(
                {
                    'name': order_item.item.name,
                    'quantity': order_item.quantity,
                }
            )
    return order_items_names_and_quantities

