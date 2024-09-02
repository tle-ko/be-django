from django.apps import AppConfig


class BojConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.boj"

    def ready(self) -> None:
        from apps.boj import services