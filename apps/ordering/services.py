"""
Module for services
"""
from django.db import transaction
from rest_framework import status

from apps.ordering.models import Order, OrderItem
from apps.storage.models import ReadyMadeProduct, Item
from apps.accounts.models import CustomUser
from apps.notices.tasks import (
    create_notification_for_barista,
    create_notification_for_client,
)
from apps.ordering.tasks import (
    update_user_bonus_points,
)
from utils.menu import (
    check_if_items_can_be_made,
    update_ingredient_stock_on_cooking,
    check_if_ready_made_product_can_be_made,
    update_ready_made_product_stock_on_cooking,
)

# ============================================================
# Actions
# ============================================================
def create_order(user_id, total_price, items, in_an_institution, spent_bonus_points=0):
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
        update_user_bonus_points.delay(user_id, total_price, spent_bonus_points)

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
        if len(order_items) != len(items):
            return None
        OrderItem.objects.bulk_create(order_items)
        order_items_names_and_quantities = get_order_items_names_and_quantities(order_items)
        order_items_names_and_quantities_str = ', '.join(
            [f"{order_item['name']} х{order_item['quantity']}" for order_item in order_items_names_and_quantities]
        )
        create_notification_for_client.delay(
            client_id=user.id,
            title=f'Ваш заказ №{order.id} принят',
            body=order_items_names_and_quantities_str,
        )
        create_notification_for_barista.delay(
            order_id=order.id,
            title=f'Заказ №{order.id} принят (в заведении), ожидайте' if in_an_institution else f'Заказ №{order.id} принят',
            body=order_items_names_and_quantities_str,
            branch_id=user.branch.id,
        )
        return order


def reorder(order_id):
    """
    Reorders order.
    """
    with transaction.atomic():
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        items = []
        for order_item in order_items:
            if order_item.ready_made_product:
                items.append(
                    {
                        'is_ready_made_product': True,
                        'item_id': order_item.ready_made_product.id,
                        'quantity': order_item.quantity,
                    }
                )
            else:
                items.append(
                    {
                        'is_ready_made_product': False,
                        'item_id': order_item.item.id,
                        'quantity': order_item.quantity,
                    }
                )
        order_create = create_order(
            user_id=order.customer.id,
            total_price=order.total_price,
            items=items,
            in_an_institution=order.in_an_institution,
        )
        return order_create


# ============================================================
# Getters
# ============================================================
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


def get_reorder_information(order_id):
    """
    Returns reorder information.
    """
    try:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return {
                'message': 'Заказ не найден.',
                'details': 'Заказ не найден.',
                'status': status.HTTP_404_NOT_FOUND,
            }
        current_branch = order.customer.branch
        try:
            order_items = OrderItem.objects.filter(order=order)
        except OrderItem.DoesNotExist:
            return {
                'message': 'Заказ не найден.',
                'details': 'Заказ не найден.',
                'status': status.HTTP_404_NOT_FOUND,
            }
        not_available_items = []
        for order_item in order_items:
            if order_item.ready_made_product:
                if check_if_ready_made_product_can_be_made(order_item.ready_made_product, current_branch, order_item.quantity):
                    continue
                else:
                    not_available_items.append(order_item.ready_made_product.name)
            else:
                if check_if_items_can_be_made(order_item.item, current_branch.id, order_item.quantity):
                    continue
                else:
                    not_available_items.append(order_item.item.name)
        if len(not_available_items) == len(order_items):
            return {
                'message': f'Заказать в заведении {current_branch.name_of_shop}?',
                'details': f'В данный момент недоступны все товары из заказа. Попробуйте позже.',
                'status': status.HTTP_400_BAD_REQUEST,
            }
        return {
            'message': f'Заказать в заведении {current_branch.name_of_shop}?',
            'details': f'В данный момент некоторые товары недоступны: {", ".join(not_available_items)}. Заказ будет сформирован с остальными товарами.',
            'status': status.HTTP_200_OK,
        } if len(not_available_items) > 0 else {
            'message': f'Заказать в заведении {current_branch.name_of_shop}?',
            'details': 'Все товары доступны.',
            'status': status.HTTP_200_OK,
        }
    except Exception as e:
        return {
            'message': 'Ошибка сервера.',
            'details': str(e),
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
