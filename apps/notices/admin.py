from django.contrib import admin
from .models import BaristaNotification

class BaristaNotificationAdmin(admin.ModelAdmin):
    list_display = ('branch', 'order_id', 'title', 'body', 'is_read', 'created_at')
    list_filter = ('branch', 'is_read', 'created_at')
    search_fields = ('branch', 'order_id', 'title', 'body', 'is_read', 'created_at')
    ordering = ('-created_at',)


admin.site.register(BaristaNotification, BaristaNotificationAdmin)