from django.db.models.signals import post_save
from django.dispatch import receiver

from problems.models import Problem
from problems.analyzers import schedule_analyze


@receiver(post_save, sender=Problem)
def auto_analyze(sender, instance: Problem, created: bool, **kwargs):
    if created:
        schedule_analyze(instance.pk)
