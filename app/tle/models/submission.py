from django.db import models

from tle.models.user import User
from tle.models.crew_activity_problem import CrewActivityProblem
from tle.models.submission_language import SubmissionLanguage


class Submission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    activity_problem = models.ForeignKey(
        CrewActivityProblem,
        on_delete=models.PROTECT,
        related_name=CrewActivityProblem.FieldName.SUBMISSIONS,
        help_text='활동 문제를 입력해주세요.',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name=User.FieldName.SUBMISSIONS,
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

    class FieldName:
        COMMENTS = 'comments'

    def __repr__(self) -> str:
        return f'{self.activity_problem.__repr__()} ← {self.user.__repr__()} ({self.language.name})'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
