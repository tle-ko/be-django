from django.db import models

from tle.models.problem import Problem
from tle.models.problem_tag import ProblemTag
from tle.models.problem_difficulty import ProblemDifficulty


class ProblemAnalysis(models.Model):
    problem = models.OneToOneField(
        Problem,
        on_delete=models.CASCADE,
        related_name=Problem.FieldName.ANALYSIS,
        help_text='문제를 입력해주세요.',
    )
    difficulty = models.IntegerField(
        help_text='문제 난이도를 입력해주세요.',
        choices=ProblemDifficulty.choices,
    )
    tags = models.ManyToManyField(
        ProblemTag,
        related_name='problems',
        help_text='문제의 DSA 태그를 입력해주세요.',
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

    def __repr__(self) -> str:
        tags = ' '.join(f'#{tag.key}' for tag in self.tags.all())
        return f'[{ProblemDifficulty(self.difficulty).label} / {self.time_complexity} / {tags}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.problem.__repr__()} ← {self.__repr__()}'
