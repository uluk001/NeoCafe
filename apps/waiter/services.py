from apps.ordering.models import Order, OrderItem
from apps.branches.models import Branch
from apps.accounts.models import CustomUser


def get_occupied_tables(branch_id):
    """
    Get occupied tables for branch.
    """
    branch = Branch.objects.get(id=branch_id)
    orders = Order.objects.filter(
        branch=branch,
        status__in=["new", "in_progress", "ready"],
        table__gt=0,
    )
    return [order.table for order in orders]


def get_free_tables(branch_id):
    """
    Get free tables for branch.
    """
    branch = Branch.objects.get(id=branch_id)
    occupied_tables = get_occupied_tables(branch_id)
    return [
        table
        for table in range(1, branch.counts_of_tables + 1)
        if table not in occupied_tables
    ]


def get_tables_availability(branch_id):
    """
    Get structuctured tables availability.
    """
    tables = {}
    free_tables = get_free_tables(branch_id)
    occupied_tables = get_occupied_tables(branch_id)
    for table in free_tables:
        tables[table] = "free"
    for table in occupied_tables:
        tables[table] = "occupied"
    sorted_tables = sorted(tables.items(), key=lambda x: x[0])
    sorted_tables = {x[0]: x[1] for x in sorted_tables}
    return sorted_tables


def is_table_free(branch_id, table_number):
    """
    Check if table is free.
    """
    try:
        if Branch.objects.get(id=branch_id).counts_of_tables > table_number > 0:
            return table_number in get_free_tables(branch_id)
        else:
            return False
    except Branch.DoesNotExist:
        return False


def get_orders_in_institution(branch_id):
    """
    Get orders in institution.
    """
    orders = Order.objects.filter(
        branch_id=branch_id,
        in_an_institution=True,
        status__in=["new", "in_progress", "ready", "canceled", "completed"],
        table__gt=0,
    ).order_by("-created_at")

    orders_list = []
    for order in orders:
        orders_list.append(
            {
                "table_number": order.table,
                "order_status": order.status,
                "order_number": order.id,
                "order_created_at": order.created_at,
            }
        )

    return orders_list


def get_table_order_details(branch_id, table_number):
    """
    Get table order details.
    """
    try:
        branch = Branch.objects.get(id=branch_id)
        order = Order.objects.get(
            branch=branch,
            table=table_number,
            status__in=["new", "in_progress", "ready"],
        )
        return order
    except Order.DoesNotExist:
        return None
