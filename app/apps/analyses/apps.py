from django.apps import AppConfig


class AnalysesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analyses"
    verbose_name = "Problems analyses"

    def ready(self) -> None:
        import apps.analyses.analyzers
