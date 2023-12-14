from ordering.models import Order, OrderItem
from django.db.models import Sum

def get_orders(branch_id, in_an_institution=True, status=Order.NEW):
    """
    Get new orders for branch.
    """
    return Order.objects.filter(
        branch_id=branch_id,
        in_an_institution=in_an_institution,
        status=status,
    ).order_by("-created_at")


def get_only_required_fields(order):
    """
    Get only required fields for order.
    """
    return {
        'id': order.id,
        'number': order.number,
        'clientNumber': order.customer.phone_number,
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


def accept_order(order_id):
    """
    Accept order.
    """
    order = Order.objects.filter(
        order_id=order_id,
        status=Order.NEW,
    )
    if not order:
        return False
    order = order.first()
    order.status = 'in_progress'
    order.save()
    return True
