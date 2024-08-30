from __future__ import annotations

from django.db.models import QuerySet
from django.utils import timezone

from crews import models


class CrewActivityService:
    @staticmethod
    def query_all(crew: models.Crew, order_by=[models.CrewActivity.field_name.START_AT]) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: crew,
        }).order_by(*order_by)

    @staticmethod
    def query_in_progress(crew: models.Crew) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: crew,
            models.CrewActivity.field_name.START_AT + '__lte': timezone.now(),
            models.CrewActivity.field_name.END_AT + '__gt': timezone.now(),
        })

    @staticmethod
    def query_has_started(crew: models.Crew) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: crew,
            models.CrewActivity.field_name.START_AT + '__lte': timezone.now(),
        })

    @staticmethod
    def query_has_ended(crew: models.Crew) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: crew,
            models.CrewActivity.field_name.END_AT + '__lt': timezone.now(),
        })

    @staticmethod
    def last_started(crew: models.Crew) -> CrewActivityService:
        """
        주의: CrewActivity.DoesNotExist를 발생시킬 수도 있습니다.
        """
        instance = models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: crew,
            models.CrewActivity.field_name.START_AT + '__lte': timezone.now(),
        }).latest()
        return CrewActivityService(instance)
