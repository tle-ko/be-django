from django.db.models.signals import ModelSignal
from django.db.models.signals import post_save


reviewed = ModelSignal(use_caching=True)
