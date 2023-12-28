"""
Models for ordering app
"""
from django.db import models
from apps.storage.models import Item
from django.utils import timezone
from apps.accounts.models import CustomUser


class Order(models.Model):
    """
    Model for orders.
    """

    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("ready", "Ready"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    ]
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Branch",
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Customer",
    )
    table = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Table number",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Status",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Completed at",
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Cancelled at",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total price",
    )
    spent_bonus_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Spent bonus points",
    )
    in_an_institution = models.BooleanField(
        default=False,
        verbose_name="In an institution",
    )

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """
    Model for order items.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Order",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Item",
        null=True,
        blank=True,
    )
    ready_made_product = models.ForeignKey(
        "storage.ReadyMadeProduct",
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Ready made product",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantity",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Created at",
    )

    def __str__(self):
        return f"Order #{self.order.id} item {self.item}"

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"
        ordering = ["-created_at"]
