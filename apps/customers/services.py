from django.db.models import F
from django.contrib.postgres.aggregates import StringAgg
from apps.branches.models import Branch
from apps.ordering.models import Order, OrderItem


def get_branch_name_and_id_list():
    """
    Get list of branches with their id and name.
    """
    branches = Branch.objects.all().only("id", "name_of_shop")
    return branches


def get_my_opened_orders_data(user):
    """
    Get opened orders of the user.
    """
    orders = Order.objects.filter(
        customer=user,
        status__in=["new", "in_progress"],
    ).only(
        "id",
        "branch__name_of_shop",
        "branch__image",
        "created_at",
    )

    return orders


def get_my_closed_orders_data(user):
    """
    Get closed orders of the user.
    """
    orders = Order.objects.filter(
        customer=user,
        status__in=["ready", "cancelled", "completed"],
    ).only(
        "id",
        "branch__name_of_shop",
        "branch__image",
        "created_at",
    )

    return orders


def get_specific_order_data(order_id):
    """
    Get specific order data.
    """
    order = (
        Order.objects.filter(
            id=order_id,
        )
        .select_related("branch")
        .first()
    )

    items = OrderItem.objects.filter(
        order=order_id,
    ).select_related(
        "item", "item__category", "ready_made_product", "ready_made_product__category"
    )

    data = {}
    data["order_id"] = order_id
    data["branch_name"] = order.branch.name_of_shop
    data["order_date"] = order.created_at.strftime("%d.%m.%Y")
    data["items"] = []
    data["order_total_price"] = order.total_price
    data["order_spent_bonus_points"] = order.spent_bonus_points
    for item in items:
        if item.item is not None:
            data["items"].append(
                {
                    "item_name": item.item.name,
                    "item_price": item.item.price,
                    "item_quantity": item.quantity,
                    "item_total_price": item.item.price * item.quantity,
                    "item_image": item.item.image,
                    "item_id": item.item.id,
                    "item_category": item.item.category.name,
                }
            )
        else:
            data["items"].append(
                {
                    "item_name": item.ready_made_product.name,
                    "item_price": item.ready_made_product.price,
                    "item_quantity": item.quantity,
                    "item_total_price": item.ready_made_product.price * item.quantity,
                    "item_image": item.ready_made_product.image,
                    "item_id": item.ready_made_product.id,
                    "item_category": item.ready_made_product.category.name,
                }
            )
    return data
