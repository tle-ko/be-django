from django.apps import AppConfig


class AnalysesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "problems.analyses"

    def ready(self) -> None:
        import problems.analyses.services
