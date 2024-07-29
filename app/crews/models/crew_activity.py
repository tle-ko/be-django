from __future__ import annotations

from django.contrib import admin
from django.db import models
from django.utils import timezone

from crews.models.crew import Crew


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    name = models.TextField(
        help_text='활동 이름을 입력해주세요. (예: "1회차")',
    )
    start_at = models.DateTimeField(
        help_text='활동 시작 일자를 입력해주세요.',
    )
    end_at = models.DateTimeField(
        help_text='활동 종료 일자를 입력해주세요.',
    )

    class field_name:
        CREW = 'crew'
        NAME = 'name'
        START_AT = 'start_at'
        END_AT = 'end_at'

    class Meta:
        ordering = ['start_at']
        get_latest_by = ['end_at']

    @classmethod
    def opened_of_crew(cls, crew: Crew) -> models.QuerySet[CrewActivity]:
        """활동 시작 전이거나 종료된 활동을 제외한 활동 목록을 반환합니다."""
        return cls.objects.filter(crew=crew, start_at__lte=timezone.now(), end_at__gte=timezone.now())

    @classmethod
    def closed_of_crew(cls, crew: Crew) -> models.QuerySet[CrewActivity]:
        """종료된 활동 목록을 반환합니다."""
        return cls.objects.filter(crew=crew, end_at__lt=timezone.now())

    @admin.display(boolean=True, description='Is Opend')
    def is_opened(self) -> bool:
        """활동이 진행 중인지 여부를 반환합니다."""
        return self.start_at <= timezone.now() <= self.end_at

    @admin.display(boolean=True, description='Is Closed')
    def is_closed(self) -> bool:
        """활동이 종료되었는지 여부를 반환합니다."""
        return self.end_at < timezone.now()

    @admin.display(description='Nth')
    def nth(self) -> int:
        """활동의 회차 번호를 반환합니다.

        이 값은 1부터 시작합니다.
        자신의 활동 시작일자보다 이전에 시작된 활동의 개수를 센 값에 1을
        더한 값을 반환하므로, 고정된 값이 아닙니다.
        """
        return self.crew.activities.filter(start_at__lte=self.start_at).count()