from django.db import models

from problems import enums
from problems.models.problem import Problem


class ProblemAnalysis(models.Model):
    problem = models.ForeignKey(
        Problem,
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
        TAGS = 'tags'
        TIME_COMPLEXITY = 'time_complexity'
        HINT = 'hint'
        CREATED_AT = 'created_at'

    class Meta:
        verbose_name_plural = 'Problem analyses'
        ordering = ['-created_at']
        get_latest_by = ['created_at']

    def __str__(self):
        return f'[Analyse of {self.problem}]'