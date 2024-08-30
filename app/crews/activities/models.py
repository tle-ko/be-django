from __future__ import annotations

from typing import Union

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from crews.enums import ProgrammingLanguageChoices
from crews.models import Crew
from problems.models import Problem
from users.models import User


class CrewActivityManager(models.Manager):
    def filter(self,
               crew: Crew = None,
               has_started: bool = None,
               in_progress: bool = None,
               *args,
               **kwargs) -> models.QuerySet[CrewActivity]:
        if crew is not None:
            assert isinstance(crew, Crew)
            kwargs[CrewActivity.field_name.CREW] = crew
        if has_started is not None:
            kwargs[CrewActivity.field_name.START_AT + '__lte'] = timezone.now()
        if in_progress is not None:
            kwargs[CrewActivity.field_name.START_AT + '__lte'] = timezone.now()
            kwargs[CrewActivity.field_name.END_AT + '__gt'] = timezone.now()
        return super().filter(*args, **kwargs)


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

    objects: _CrewActivityManager = CrewActivityManager()

    class field_name:
        CREW = 'crew'
        NAME = 'name'
        START_AT = 'start_at'
        END_AT = 'end_at'

    class Meta:
        ordering = ['start_at']
        get_latest_by = ['end_at']

    def __str__(self) -> str:
        return f'[{self.pk}: "{self.name}"@"{self.crew.display_name()}" ({self.start_at.date()} ~ {self.end_at.date()})]'

    def is_in_progress(self) -> bool:
        return self.has_started() and not self.has_ended()

    def has_started(self) -> bool:
        return self.start_at <= timezone.now()

    def has_ended(self) -> bool:
        return self.end_at < timezone.now()


class CrewActivityProblemManager(models.Manager):
    def crew(self, crew: Crew) -> _CrewActivityProblemManager:
        return self.filter(**{CrewActivityProblem.field_name.CREW: crew})


class CrewActivityProblem(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    activity = models.ForeignKey(
        CrewActivity,
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

    objects: _CrewActivityProblemManager = CrewActivityProblemManager()

    class field_name:
        # related fields
        SUBMISSIONS = 'submissions'
        # fields
        CREW = 'crew'
        ACTIVITY = 'activity'
        PROBLEM = 'problem'
        ORDER = 'order'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'order'],
                name='unique_order_per_activity_problem',
            ),
        ]
        ordering = ['order']

    def save(self, *args, **kwargs) -> None:
        assert self.crew == self.activity.crew
        return super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivitySubmission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    problem = models.ForeignKey(
        CrewActivityProblem,
        on_delete=models.PROTECT,
        help_text='활동 문제를 입력해주세요.',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='유저를 입력해주세요.',
    )
    code = models.TextField(
        help_text='유저의 코드를 입력해주세요.',
    )
    language = models.TextField(
        choices=ProgrammingLanguageChoices.choices,
        help_text='유저의 코드 언어를 입력해주세요.',
    )
    is_correct = models.BooleanField(
        help_text='유저의 코드가 정답인지 여부를 입력해주세요.',
    )
    is_help_needed = models.BooleanField(
        help_text='유저의 코드에 도움이 필요한지 여부를 입력해주세요.',
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class field_name:
        PROBLEM = 'problem'
        USER = 'user'
        CODE = 'code'
        LANGUAGE = 'language'
        IS_CORRECT = 'is_correct'
        IS_HELP_NEEDED = 'is_help_needed'
        CREATED_AT = 'created_at'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.problem}  ← {self.user}]'


_CrewActivityManager = Union[CrewActivityManager, models.Manager[CrewActivity]]
_CrewActivityProblemManager = Union[CrewActivityProblemManager,
                                    models.Manager[CrewActivityProblem]]
