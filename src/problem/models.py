from django.db import models

from core.models import *
from user.models import User


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


class ProblemAnalysis(models.Model):
    problem = models.ForeignKey(
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
