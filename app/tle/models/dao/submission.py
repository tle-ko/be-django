from django.db import models

from users.models import User
from tle.models.dao.crew_activity_problem import CrewActivityProblem
from tle.models.dao.submission_language import SubmissionLanguage


class Submission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    activity_problem = models.ForeignKey(
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
    language = models.ForeignKey(
        SubmissionLanguage,
        on_delete=models.PROTECT,
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
        ACTIVITY_PROBLEM = 'activity_problem'
        USER = 'user'
        CODE = 'code'
        LANGUAGE = 'language'
        IS_CORRECT = 'is_correct'
        IS_HELP_NEEDED = 'is_help_needed'
        CREATED_AT = 'created_at'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['created_at']

    def __repr__(self) -> str:
        return f'{self.activity_problem.__repr__()} ← {self.user.__repr__()} ({self.language.name})'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
