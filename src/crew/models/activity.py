from django.core.validators import MinValueValidator
from django.db import models

from core.models import Language
from crew.models.crew import Crew
from problem.models import Problem
from user.models import User


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    start_at = models.DateTimeField(
        help_text=(
            '활동 시작 일자를 입력해주세요.'
        ),
    )
    end_at = models.DateTimeField(
        help_text=(
            '활동 종료 일자를 입력해주세요.'
        ),
    )

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← [{self.start_at.date()} ~ {self.end_at.date()}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblem(models.Model):
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.CASCADE,
        related_name='problems',
        help_text=(
            '활동을 입력해주세요.'
        ),
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        related_name='activities',
        help_text=(
            '문제를 입력해주세요.'
        ),
    )
    order = models.IntegerField(
        help_text=(
            '문제 순서를 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 다른 문제 순서와 겹치지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblemSubmission(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    activity_problem = models.ForeignKey(
        CrewActivityProblem,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=(
            '활동 문제를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    code = models.TextField(
        help_text=(
            '유저의 코드를 입력해주세요.'
        ),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name='submissions',
        help_text=(
            '유저의 코드 언어를 입력해주세요.'
        ),
    )
    is_correct = models.BooleanField(
        help_text=(
            '유저의 코드가 정답인지 여부를 입력해주세요.'
        ),
    )
    is_help_needed = models.BooleanField(
        help_text=(
            '유저의 코드에 도움이 필요한지 여부를 입력해주세요.'
        ),
        default=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'{self.activity_problem.__repr__()} ← {self.user.__repr__()} ({self.language.name})'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


class CrewActivityProblemSubmissionComment(models.Model):
    submission = models.ForeignKey(
        CrewActivityProblemSubmission,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=(
            '제출을 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    content = models.TextField(
        help_text=(
            '댓글을 입력해주세요.'
        ),
    )
    line_number_start = models.IntegerField(
        help_text=(
            '댓글 시작 라인을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
        ],
    )
    line_number_end = models.IntegerField(
        help_text=(
            '댓글 종료 라인을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 시작 라인보다 작지 않도록 검사
            # TODO: 코드 라인 수보다 크지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        line_range = f'L{self.line_number_start}:L{self.line_number_end}'
        return f'{self.submission.__repr__()} ← {self.user.__repr__()} {line_range} "{self.content}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
