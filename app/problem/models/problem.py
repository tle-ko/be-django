from dataclasses import dataclass
from typing import List

from django.db import models

from account.models import User


class Problem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='problems',
        help_text=(
            '이 문제를 추가한 사용자를 입력해주세요.'
        ),
        null=True,
    )
    title = models.CharField(
        max_length=100,
        help_text=(
            '문제 이름을 입력해주세요.'
        ),
        blank=False,
    )
    link = models.URLField(
        help_text=(
            '문제 링크를 입력해주세요. (선택)'
        ),
        blank=True,
    )
    description = models.TextField(
        help_text=(
            '문제 설명을 입력해주세요.'
        ),
        blank=False,
    )
    input_description = models.TextField(
        help_text=(
            '문제 입력 설명을 입력해주세요.'
        ),
        blank=True,
    )
    output_description = models.TextField(
        help_text=(
            '문제 출력 설명을 입력해주세요.'
        ),
        blank=True,
    )
    memory_limit = models.FloatField(
        help_text=(
            '문제 메모리 제한을 입력해주세요. (MB 단위)'
        ),
    )
    time_limit = models.FloatField(
        help_text=(
            '문제 시간 제한을 입력해주세요. (초 단위)'
        ),
        default=1.0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'[{self.title}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ← {self.user.__repr__()}'


@dataclass
class ProblemDTO:
    title: str
    description: str
    input_description: str
    output_description: str
    memory_limit: float
    time_limit: float
