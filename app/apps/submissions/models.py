from django.core.validators import MinValueValidator
from django.db import models

from apps.activities.models import CrewActivityProblemDAO
from apps.crews.enums import ProgrammingLanguageChoices
from users.models import User


class SubmissionDAO(models.Model):
    # TODO: 같은 문제에 여러 번 제출 하는 것을 막기 위한 로직 추가
    problem = models.ForeignKey(
        CrewActivityProblemDAO,
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
        get_latest_by = ['created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.problem}  ← {self.user}]'


class SubmissionCommentDAO(models.Model):
    submission = models.ForeignKey(
        SubmissionDAO,
        on_delete=models.CASCADE,
        help_text='제출을 입력해주세요.',
    )
    content = models.TextField(
        max_length=1000,
        help_text='댓글을 입력해주세요.',
        blank=False,
        null=False,
    )
    line_number_start = models.IntegerField(
        help_text='댓글 시작 라인을 입력해주세요.',
        validators=[
            MinValueValidator(1),
        ],
    )
    line_number_end = models.IntegerField(
        help_text='댓글 종료 라인을 입력해주세요.',
        validators=[
            MinValueValidator(1),
            # TODO: 시작 라인보다 작지 않도록 검사
            # TODO: 코드 라인 수보다 크지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='유저를 입력해주세요.',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class field_name:
        SUBMISSION = 'submission'
        CONTENT = 'content'
        LINE_NUMBER_START = 'line_number_start'
        LINE_NUMBER_END = 'line_number_end'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.submission} ← {self.created_by}] L{self.line_number_start}:L{self.line_number_end}'
