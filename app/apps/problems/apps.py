from django.apps import AppConfig


class ProblemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.problems"

    def ready(self) -> None:
        from apps.problems import analyzers
