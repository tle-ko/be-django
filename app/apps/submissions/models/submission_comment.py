from django.core.validators import MinValueValidator
from django.db import models

from apps.submissions.models.submission import Submission
from users.models import User


class SubmissionComment(models.Model):
    submission = models.ForeignKey(
        Submission,
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
