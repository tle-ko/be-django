from __future__ import annotations

from django.db import models

from apps.problems.models import ProblemDAO

from . import enums


class ProblemTagDAO(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 키를 입력해주세요. (최대 20자)',
    )
    name_ko = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(국문)을 입력해주세요. (최대 50자)',
    )
    name_en = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(영문)을 입력해주세요. (최대 50자)',
    )

    class field_name:
        KEY = 'key'
        NAME_KO = 'name_ko'
        NAME_EN = 'name_en'

    class Meta:
        ordering = ['key']

    def __repr__(self) -> str:
        return f'[#{self.key}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ({self.name_ko})'


class ProblemTagRelationDAO(models.Model):
    parent = models.ForeignKey(
        ProblemTagDAO,
        on_delete=models.CASCADE,
        related_name='parent'
    )
    child = models.ForeignKey(
        ProblemTagDAO,
        on_delete=models.CASCADE,
        related_name='child'
    )

    class field_name:
        PARENT = 'parent'
        CHILD = 'child'

    def __str__(self) -> str:
        return f'{self.pk} : #{self.parent.key} <- #{self.child.key}'


class ProblemAnalysisDAO(models.Model):
    problem = models.ForeignKey(
        ProblemDAO,
        on_delete=models.CASCADE,
        help_text='문제를 입력해주세요.',
    )
    difficulty = models.IntegerField(
        help_text='문제 난이도를 입력해주세요.',
        choices=enums.ProblemDifficulty.choices,
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
    )
    hint = models.JSONField(
        help_text='문제 힌트를 입력해주세요. Step-by-step 으로 입력해주세요.',
        validators=[
            # TODO: 힌트 검증 로직 추가
        ],
        blank=False,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        PROBLEM = 'problem'
        DIFFICULTY = 'difficulty'
        TIME_COMPLEXITY = 'time_complexity'
        HINT = 'hint'
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
        ProblemTagDAO,
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
