"""
Module for services
"""
from django.db import transaction
from rest_framework import status

from apps.ordering.models import Order, OrderItem
from apps.storage.models import (
    ReadyMadeProduct, Item, Composition,
    AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch
)
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
def create_order(user_id, total_price, items, in_an_institution, spent_bonus_points=0, pass_check_if_all_items_can_be_made=False, table_number=0):
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
            table=table_number,
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
        if not pass_check_if_all_items_can_be_made and len(order_items) != len(items):
            return None
        OrderItem.objects.bulk_create(order_items)
        order_items_names_and_quantities = get_order_items_names_and_quantities(order_items)
        order_items_names_and_quantities_str = ', '.join(
            [f"{order_item['name']} х{order_item['quantity']}" for order_item in order_items_names_and_quantities]
        )
        create_notification_for_client.delay(
            client_id=user.id,
            title=f'Ваш заказ №{order.id} создан' if user.position == 'waiter' else f'Заказ №{order.id} создан',
            body=order_items_names_and_quantities_str,
        )
        create_notification_for_barista.delay(
            order_id=order.id,
            title=f'Заказ №{order.id} создан (в заведении), ожидайте' if in_an_institution else f'Заказ №{order.id} создан',
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
            pass_check_if_all_items_can_be_made=True,
        )
        return order_create


def add_item_to_order(order_id, item_id, is_ready_made_product, quantity=1):
    """
    Adds item to order.
    """
    with transaction.atomic():
        order = Order.objects.get(id=order_id)
        print(order.status)
        if not check_if_order_new(order):
            print('Order is not new.')
            return None
        print('Order is new.')
        if is_ready_made_product:
            ready_made_product = ReadyMadeProduct.objects.get(id=item_id)
            if check_if_ready_made_product_can_be_made(ready_made_product, order.customer.branch, quantity):
                try:
                    order_item = OrderItem.objects.get(
                        order=order,
                        ready_made_product=ready_made_product,
                    )
                    order_item.quantity += quantity
                    order_item.save()
                except OrderItem.DoesNotExist:
                    OrderItem.objects.create(
                        order=order,
                        ready_made_product=ready_made_product,
                        quantity=quantity,
                    )
                update_ready_made_product_stock_on_cooking(ready_made_product, order.customer.branch, quantity)
                order.total_price += ready_made_product.price * quantity
                order.save()
                return order  # Return the Order object
            else:
                return None
        else:
            try:
                item = Item.objects.get(id=item_id)
                if check_if_items_can_be_made(item, order.customer.branch.id, quantity):
                    try:
                        order_item = OrderItem.objects.get(
                            order=order,
                            item=item,
                        )
                        order_item.quantity += quantity
                        order_item.save()
                    except OrderItem.DoesNotExist:
                        OrderItem.objects.create(
                            order=order,
                            item=item,
                            quantity=quantity,
                        )
                    update_ingredient_stock_on_cooking(item, order.customer.branch, quantity)
                    order.total_price += item.price * quantity
                    order.save()
                    return order  # Return the Order object
                else:
                    return None
            except Item.DoesNotExist:
                print('Item does not exist.')
                return None


def check_if_order_new(order):
    """
    Checks if order is new.
    """
    return order.status == 'new'


def remove_order_item(order_item_id):
    """
    Removes order item.
    """
    with transaction.atomic():
        order_item = OrderItem.objects.get(id=order_item_id)
        order = order_item.order
        if not check_if_order_new(order):
            return None
        item_price = order_item.item.price
        order_item.quantity -= 1
        if order_item.quantity == 0:
            order_item.delete()
        else:
            order_item.save()
        if order_item.ready_made_product:
            return_ready_made_product_to_storage(
                order_item.ready_made_product,
                order_item.order.branch_id,
                1,
            )
        else:
            return_item_ingredients_to_storage(
                order_item.item_id,
                order_item.order.branch_id,
                1,
            )
        order.total_price -= item_price
        order.save()
        return order

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


def return_item_ingredients_to_storage(item_id, branch_id, quantity):
    """
    Return item ingredients to storage.
    """
    try:
        compositions = Composition.objects.filter(item_id=item_id).select_related('ingredient')
        ingredients_to_update = []

        for composition in compositions:
            available_ingredient = AvailableAtTheBranch.objects.get(
                branch_id=branch_id,
                ingredient_id=composition.ingredient_id
            )
            available_ingredient.quantity += composition.quantity * quantity
            ingredients_to_update.append(available_ingredient)

        AvailableAtTheBranch.objects.bulk_update(ingredients_to_update, ['quantity'])
        return "Updated successfully."
    except Exception as e:
        raise e


def return_ready_made_product_to_storage(ready_made_product, branch_id, quantity):
    """
    Return ready made product to storage.
    """
    try:
        available_product = ReadyMadeProductAvailableAtTheBranch.objects.get(
            branch_id=branch_id,
            ready_made_product=ready_made_product
        )
        available_product.quantity += quantity
        available_product.save()
        return "Updated successfully."
    except Exception as e:
        raise e


def return_order_item_to_storage(order_item):
    """
    Return order item to storage.
    """
    try:
        if order_item.ready_made_product:
            return_ready_made_product_to_storage(
                order_item.ready_made_product,
                order_item.order.branch_id,
                order_item.quantity,
            )
        else:
            return_item_ingredients_to_storage(
                order_item.item_id,
                order_item.order.branch_id,
                order_item.quantity,
            )
        return "Updated successfully."
    except Exception as e:
        raise e


def return_to_storage(order_id):
    """
    Return order to storage.
    """
    try:
        order_items = OrderItem.objects.filter(order_id=order_id)
        for order_item in order_items:
            return_order_item_to_storage(order_item)
        return "Returned successfully."
    except Exception as e:
        raise e
