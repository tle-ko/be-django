from __future__ import annotations

from django.db import models

from apps.crews.enums import ProgrammingLanguageChoices
from apps.activities.models import CrewActivity
from apps.activities.models import CrewActivityProblem
from users.models import User


class SubmissionManager(models.Manager):
    def filter(self,
               activity: CrewActivity = None,
               activity_problem: CrewActivityProblem = None,
               user: User = None,
               *args, **kwargs) -> models.QuerySet[Submission]:
        if activity is not None:
            kwargs[Submission.field_name.ACTIVITY] = activity
        if activity_problem is not None:
            kwargs[Submission.field_name.PROBLEM] = activity_problem
        if user is not None:
            kwargs[Submission.field_name.USER] = user
        return super().filter(*args, **kwargs)


class Submission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.PROTECT,
    )
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

    objects: SubmissionManager = SubmissionManager()

    class field_name:
        ACTIVITY = 'activity'
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
