from django.db.models.signals import post_save
from django.dispatch import receiver

from problems import models
from problems import services


@receiver(post_save, sender=models.Problem)
def schedule_analyze(sender, instance: models.Problem, **kwargs):
    service = services.get_problem_service(instance)
    service.analyze()
