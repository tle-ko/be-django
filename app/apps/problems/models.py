from __future__ import annotations

from django.db import models

from apps.boj.models import BOJTagDAO
from users.models import User

from . import enums


class ProblemDAO(models.Model):
    title = models.CharField(
        max_length=100,
        help_text='문제 이름을 입력해주세요.',
    )
    link = models.URLField(
        help_text='문제 링크를 입력해주세요. (선택)',
        blank=True,
    )
    description = models.TextField(
        help_text='문제 설명을 입력해주세요.',
    )
    input_description = models.TextField(
        help_text='문제 입력 설명을 입력해주세요.',
    )
    output_description = models.TextField(
        help_text='문제 출력 설명을 입력해주세요.',
    )
    memory_limit = models.FloatField(
        help_text='문제 메모리 제한을 입력해주세요. (MB 단위)',
    )
    memory_limit_unit = models.TextField(
        choices=enums.Unit.choices,
        default=enums.Unit.MEGA_BYTE,
    )
    time_limit = models.FloatField(
        help_text='문제 시간 제한을 입력해주세요. (초 단위)',
    )
    time_limit_unit = models.TextField(
        choices=enums.Unit.choices,
        default=enums.Unit.SECOND,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        help_text='이 문제를 추가한 사용자를 입력해주세요.',
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class field_name:
        TITLE = 'title'
        LINK = 'link'
        DESCRIPTION = 'description'
        INPUT_DESCRIPTION = 'input_description'
        OUTPUT_DESCRIPTION = 'output_description'
        MEMORY_LIMIT = 'memory_limit'
        MEMORY_LIMIT_UNIT = 'memory_limit_unit'
        TIME_LIMIT = 'time_limit'
        TIME_LIMIT_UNIT = 'time_limit_unit'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.title}]'


class ProblemAnalysisDAO(models.Model):
    problem = models.ForeignKey(
        ProblemDAO,
        on_delete=models.CASCADE,
        help_text='문제를 입력해주세요.',
    )
    difficulty = models.IntegerField(
        help_text='문제 난이도를 입력해주세요.',
        choices=enums.ProblemDifficulty.choices,
        default=enums.ProblemDifficulty.UNDER_ANALYSIS,
    )
    time_complexity = models.CharField(
        max_length=100,
        help_text=(
            '문제 시간 복잡도를 입력해주세요. ',
            '예) O(1), O(n), O(n^2), O(V \log E) 등',
        ),
        validators=[
            # TODO: 시간 복잡도 검증 로직 추가
        ],
        blank=True,
        null=False,
        default='',
    )
    hints = models.JSONField(
        help_text='문제 힌트를 입력해주세요. Step-by-step 으로 입력해주세요.',
        validators=[
            # TODO: 힌트 검증 로직 추가
        ],
        blank=False,
        null=False,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        PROBLEM = 'problem'
        DIFFICULTY = 'difficulty'
        TIME_COMPLEXITY = 'time_complexity'
        HINTS = 'hints'
        CREATED_AT = 'created_at'

    class Meta:
        verbose_name_plural = 'Problem analyses'
        ordering = ['-created_at']
        get_latest_by = ['created_at']

    def __str__(self):
        return f'[Analyse of {self.problem}]'


class ProblemAnalysisTagDAO(models.Model):
    analysis = models.ForeignKey(
        ProblemAnalysisDAO,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    tag = models.ForeignKey(
        BOJTagDAO,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        help_text='문제의 DSA 태그를 입력해주세요.',
    )

    class field_name:
        ANALYSIS = 'analysis'
        TAG = 'tag'

    def __str__(self):
        return f'{self.analysis.problem} #{self.tag}'
