from django.db import models

from problems.models.problem_analysis import ProblemAnalysis
from problems.models.problem_tag import ProblemTag


class ProblemAnalysisTag(models.Model):
    analysis = models.ForeignKey(
        ProblemAnalysis,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    tag = models.ForeignKey(
        ProblemTag,
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
