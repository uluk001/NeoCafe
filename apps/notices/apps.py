from django.apps import AppConfig


class NoticesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notices"

    def ready(self):
        import apps.notices.signals  # noqa
        import apps.notices.tasks
