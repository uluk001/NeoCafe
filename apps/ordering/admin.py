"""
Module for admin models for ordering app.
"""
from django.contrib import admin
from apps.ordering.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline model for order items.
    """
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    """
    Admin model for orders.
    """
    list_display = [
        "id",
        "customer",
        "created_at",
        "total_price",
    ]
    list_filter = ["created_at", "status"]
    search_fields = ["customer__user__username"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
