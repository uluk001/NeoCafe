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
from apps.ordering.services import (
    get_order_items_names_and_quantities,
    return_to_storage,
)

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
        'clientNumber': str(order.customer.phone_number) if not order.customer.position == 'waiter' else order.customer.first_name,
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
            'name': order_item.item.name if order_item.ready_made_product is None else order_item.ready_made_product.name,
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
            'name': order_item.item.name if order_item.ready_made_product is None else order_item.ready_made_product.name,
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
    return_to_storage(order_id)
    return True


def complete_order(order_id):
    """
    Complete order.
    """
    order = Order.objects.filter(
        id=order_id,
        status='ready',
    )
    if not order:
        return False
    order = order.first()
    order.status = 'completed'
    order.save()
    order_items = get_order_items_str(order.id)
    create_notification_for_client.delay(
        order.customer.id,
        'Бариста завершил заказ' if not order.customer.position == 'waiter' else 'Закрытие счета',
        f'Ваш заказ №{order.id} завершен. {order_items}' if not order.customer.position == 'waiter' else f'Стол №{order.table} закрыт',
    )
    return True


def make_order_ready(order_id):
    """
    Make order ready.
    """
    order = Order.objects.filter(
        id=order_id,
        status='in_progress',
    )
    if not order:
        return False
    order = order.first()
    order.status = 'ready'
    order.save()
    order_items = get_order_items_str(order.id)
    create_notification_for_client.delay(
        order.customer.id,
        'Заказ готов',
        f'Ваш заказ №{order.id} готов. {order_items}',
    )
    return True
