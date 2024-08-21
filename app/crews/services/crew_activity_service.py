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

    def __init__(self, instance: models.CrewActivity) -> None:
        assert isinstance(instance, models.CrewActivity)
        self.instance = instance

    def query_previous(self) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: self.instance.crew,
            models.CrewActivity.field_name.START_AT+'__lt': self.instance.start_at,
        })

    def nth(self) -> int:
        """활동의 회차 번호를 반환합니다.

        이 값은 1부터 시작합니다.
        자신의 활동 시작일자보다 이전에 시작된 활동의 개수를 센 값에 1을
        더한 값을 반환하므로, 고정된 값이 아닙니다.

        느린 연산입니다.
        한 번에 여러 회차 번호들을 조회하기 위해 이 함수를 사용하는 것은 권장하지 않습니다.
        """
        return self.query_previous().count()+1

    def is_in_progress(self) -> bool:
        """활동이 진행 중인지 여부를 반환합니다."""
        return self.has_started() and not self.has_ended()

    def has_started(self) -> bool:
        """활동이 열린적이 있는지 여부를 반환합니다.."""
        return self.instance.start_at <= timezone.now()

    def has_ended(self) -> bool:
        """활동이 종료되었는지 여부를 반환합니다."""
        return self.instance.end_at < timezone.now()
