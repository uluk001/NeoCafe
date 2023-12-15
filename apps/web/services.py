from apps.ordering.models import Order, OrderItem
from django.db.models import Sum
from apps.storage.models import (
    AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch,
    Composition,
)
from asgiref.sync import sync_to_async
from apps.notices.tasks import (
    create_notification_for_barista, create_notification_for_client,
)
from apps.ordering.services import get_order_items_names_and_quantities

# ============================================================
# Getters
# ============================================================
def get_orders(branch_id, in_an_institution=True, status='new'):
    """
    Get new orders for branch.
    """
    return list(Order.objects.filter(
        branch_id=branch_id,
        in_an_institution=in_an_institution,
        status=status,
    ).order_by("-created_at"))


def get_only_required_fields(order):
    """
    Get only required fields for order.
    """
    return {
        'id': order.id,
        'number': order.id,
        'clientNumber': str(order.customer.phone_number),  # Convert PhoneNumber to string
        'items': get_order_items(order),
        'status': order.status,
    }

def get_order_items(order):
    """
    Get order items for order.
    """
    order_items = OrderItem.objects.filter(order=order)
    items = []
    for order_item in order_items:
        items.append({
            'id': order_item.id,
            'name': order_item.item.name,
            'quantity': order_item.quantity,
        })
    return items


def get_order_items(order):
    """
    Get order items for order.
    """
    order_items = OrderItem.objects.filter(order=order)
    items = []
    for order_item in order_items:
        items.append({
            'id': order_item.id,
            'name': order_item.item.name,
            'quantity': order_item.quantity,
        })
    return items


def get_order_items_str(order_id):
    """
    Get order items string.
    """
    order_items = OrderItem.objects.filter(order=order_id)
    order_items_names_and_quantities = get_order_items_names_and_quantities(
        order_items,
    )
    order_items_names_and_quantities_str = ', '.join(
        [
            f'{item["name"]} - {item["quantity"]}'
            for item in order_items_names_and_quantities
        ]
    )
    return order_items_names_and_quantities_str


# ============================================================
# Actions
# ============================================================
def accept_order(order_id):
    """
    Accept order and change status to in_progress.
    """
    order = Order.objects.filter(
        id=order_id,
        status='new',
    )
    if not order:
        return False
    order = order.first()
    order.status = 'in_progress'
    order.save()
    order_items = get_order_items_str(order.id)
    create_notification_for_client.delay(
        client_id=order.customer.id,
        title='Бариста принял заказ',
        body=f'Ваш заказ №{order.id} принят. {order_items}',
    )
    return True


def cancel_order(order_id):
    """
    Cancel order and return ingredients to storage.
    """
    order = Order.objects.filter(
        id=order_id,
        status='new',
    )
    if not order:
        return False
    order = order.first()
    order.status = 'canceled'
    order.save()
    order_items = get_order_items_str(order.id)
    create_notification_for_client.delay(
        client_id=order.customer.id,
        title='Бариста отменил заказ',
        body=f'Ваш заказ №{order.id} отменен. {order_items}',
    )
    return_ingredients(order_id)
    return True


def complete_order(order_id):
    """
    Complete order.
    """
    order = Order.objects.filter(
        order_id=order_id,
        status='in_progress',
    )
    if not order:
        return False
    order = order.first()
    order.status = 'completed'
    order.save()
    order_items = get_order_items_str(order.id)
    create_notification_for_client.delay(
        order.customer.id,
        'Бариста завершил заказ',
        f'Ваш заказ №{order.id} завершен. {order_items}',
    )
    return True


def return_ingredients(order_id):
    """
    Return ingredients to storage after canceling order.
    """
    try:
        order = Order.objects.filter(id=order_id).first()
    except Order.DoesNotExist:
        return False
    branch = order.branch
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        if order_item.ready_made_product:
            availables = ReadyMadeProductAvailableAtTheBranch.objects.filter(
                branch=branch,
                ready_made_product=order_item.ready_made_product,
            )
            available = availables.first()
            available.quantity += order_item.quantity
            available.save()
        else:
            for composition in order_item.item.compositions.all():
                availables = AvailableAtTheBranch.objects.filter(
                    branch=branch,
                    ingredient=composition.ingredient,
                )
                available = availables.first()
                available.quantity += composition.quantity * order_item.quantity
                available.save()
    return True
