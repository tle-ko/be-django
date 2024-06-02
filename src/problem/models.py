from django.db import models

from user.models import User


class ProblemDifficulty(models.IntegerChoices):
    EASY = 1, '쉬움'
    NORMAL = 2, '보통'
    HARD = 3, '어려움'


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
    memory_limit = models.IntegerField(
        help_text=(
            '문제 메모리 제한을 입력해주세요. (바이트 단위)'
        ),
    )
    time_limit = models.IntegerField(
        help_text=(
            '문제 시간 제한을 입력해주세요. (밀리 초 단위)'
        ),
        default=1000,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemMeta(models.Model):
    problem = models.OneToOneField(
        Problem,
        on_delete=models.CASCADE,
        related_name='meta',
        help_text=(
            '문제를 입력해주세요.'
        ),
    )
    difficulty = models.IntegerField(
        help_text=(
            '문제 난이도를 입력해주세요.'
        ),
        choices=ProblemDifficulty.choices,
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
    # TODO: tags 필드 추가
    # TODO: 사용자가 추가한 정보인지 확인하는 필드 추가
    # TODO: 변경 이력을 저장하는 필드 추가
