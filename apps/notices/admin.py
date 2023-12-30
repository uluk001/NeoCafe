from django.contrib import admin
from .models import (
    BaristaNotification,
    ClentNotification, Reminder,
    AdminNotification,
)


class BaristaNotificationAdmin(admin.ModelAdmin):
    list_display = ("branch", "order_id", "title", "body", "is_read", "created_at")
    list_filter = ("branch", "is_read", "created_at")
    search_fields = ("branch", "order_id", "title", "body", "is_read", "created_at")
    ordering = ("-created_at",)


class ClentNotificationAdmin(admin.ModelAdmin):
    list_display = ("client_id", "title", "body", "created_at")
    list_filter = ("client_id", "created_at")
    search_fields = ("client_id", "title", "body", "created_at")
    ordering = ("-created_at",)


class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "branch", "date_of_notification")
    list_filter = ("branch", "date_of_notification")


class ReminderAdmin(admin.ModelAdmin):
    list_display = ("content", "branch", "date_of_reminder")
    list_filter = ("branch", "date_of_reminder")


admin.site.register(ClentNotification, ClentNotificationAdmin)
admin.site.register(BaristaNotification, BaristaNotificationAdmin)
admin.site.register(AdminNotification, AdminNotificationAdmin)
admin.site.register(Reminder, ReminderAdmin)
