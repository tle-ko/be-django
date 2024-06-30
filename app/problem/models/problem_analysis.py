from django.db import models

from .difficulty import Difficulty
from .problem import Problem
from .tag import Tag


class ProblemAnalysis(models.Model):
    problem = models.OneToOneField(
        Problem,
        on_delete=models.CASCADE,
        related_name='analysis',
        help_text=(
            '문제를 입력해주세요.'
        ),
    )
    difficulty = models.IntegerField(
        help_text=(
            '문제 난이도를 입력해주세요.'
        ),
        choices=Difficulty.choices,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='problems',
        help_text=(
            '문제의 DSA 태그를 입력해주세요.'
        ),
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
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: 사용자가 추가한 정보인지 확인하는 필드 추가

    def __repr__(self) -> str:
        tags = ' '.join(f'#{tag.key}' for tag in self.tags.all())
        return f'[{Difficulty(self.difficulty).label} / {self.time_complexity} / {tags}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.problem.__repr__()} ← {self.__repr__()}'
