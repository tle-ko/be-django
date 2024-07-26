from django.db import models

from problems.models.problem import Problem
from problems.models.problem_analysis import ProblemAnalysis


class ProblemAnalysisQueue(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text='문제를 입력해주세요.',
    )
    analysis = models.OneToOneField(
        ProblemAnalysis,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='문제 분석 결과를 입력해주세요.',
    )
    is_analyzing = models.BooleanField(
        default=False,
        help_text='문제 분석이 완료되었는지 여부를 입력해주세요.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        PROBLEM = 'problem'
        ANALYSIS = 'analysis'
        IS_ANALYZING = 'is_analyzing'
        CREATED_AT = 'created_at'

    class Meta:
        ordering = ['created_at']
