from django.db import transaction
from django.db.models import signals
from django.dispatch import receiver

from .models import (
    Problem,
    Analysis,
)
from .services import get_analyser


@receiver(signals.post_save, sender=Problem)
def problem_on_post_save(sender, instance: Problem, created: bool, **kwargs):
    if not created:
        return
    analyser = get_analyser()
    analysis_dto = analyser.analyze(instance)
    with transaction.atomic():
        analysis = Analysis.objects.create(
            problem=instance,
            difficulty=analysis_dto.difficulty,
            tags=analysis_dto.tags,
            time_complexity=analysis_dto.time_complexity,
            hint=analysis_dto.hint,
        )
        analysis.save()
        instance.analysis = analysis
        instance.save()
