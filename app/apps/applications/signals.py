from django.db.models.signals import ModelSignal


reviewed = ModelSignal(use_caching=True)
