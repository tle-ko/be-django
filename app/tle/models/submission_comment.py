from django.core.validators import MinValueValidator
from django.db import models

from tle.models.user import User
from tle.models.submission import Submission


class SubmissionComment(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name=Submission.FieldName.COMMENTS,
        help_text='제출을 입력해주세요.',
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
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        line_range = f'L{self.line_number_start}:L{self.line_number_end}'
        return f'{self.submission.__repr__()} ← {self.created_by.__repr__()} {line_range} "{self.content}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
