from django.apps import AppConfig


class ProblemsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.problems"

    def ready(self) -> None:
        import apps.analyses.analyzers
