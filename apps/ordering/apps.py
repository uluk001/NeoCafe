from django.apps import AppConfig


class OrderingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ordering"

    def ready(self):
        import apps.ordering.signals
        import apps.ordering.tasks
