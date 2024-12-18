from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.crews.models import CrewDAO
from apps.problems.proxy import Problem


class CrewActivityDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
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
        verbose_name = 'Crew Activity'
        verbose_name_plural = 'Crew Activities'
        ordering = ['start_at']
        get_latest_by = ['end_at']

    def __str__(self) -> str:
        return f'[{self.pk}: "{self.name}"@"{self.crew.name}" ({self.start_at.date()} ~ {self.end_at.date()})]'

    def is_in_progress(self) -> bool:
        return self.has_started() and not self.has_ended()

    def has_started(self) -> bool:
        return self.start_at <= timezone.now()

    def has_ended(self) -> bool:
        return self.end_at < timezone.now()


class CrewActivityProblemDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    activity = models.ForeignKey(
        CrewActivityDAO,
        on_delete=models.CASCADE,
        help_text='활동을 입력해주세요.',
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        help_text='문제를 입력해주세요.',
    )
    order = models.IntegerField(
        help_text='문제 순서를 입력해주세요.',
        validators=[
            MinValueValidator(1),
        ],
    )

    class field_name:
        # related fields
        SUBMISSIONS = 'submissions'
        # fields
        CREW = 'crew'
        ACTIVITY = 'activity'
        PROBLEM = 'problem'
        ORDER = 'order'

    class Meta:
        verbose_name = 'Crew Activity Problem'
        verbose_name_plural = 'Crew Activity Problems'
        ordering = ['order']
        unique_together = ['activity', 'problem']

    def save(self, *args, **kwargs) -> None:
        assert self.crew == self.activity.crew
        return super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
