from django.db import models
from apps.branches.models import Branch


class BaristaNotification(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClentNotification(models.Model):
    client_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=255, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_id} - {self.title}"


class AdminNotification(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_of_notification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    content = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_of_reminder = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date_of_reminder"]
