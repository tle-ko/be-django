from django.core.validators import MinValueValidator
from django.db import models

from boj.models import BOJLevel
from core.models import Language
from user.models import User


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '크루 이름을 입력해주세요. (최대 20자)'
        ),
    )
    emoji = models.CharField(
        max_length=2,
        help_text=(
            '크루 아이콘을 입력해주세요. (이모지)'
        ),
        validators=[
            # TODO: 이모지 형식 검사
        ],
        null=True,
        blank=True,
    )
    captain = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='crews_as_captain',
        help_text=(
            '크루장을 입력해주세요.'
        ),
    )
    notice = models.TextField(
        help_text=(
            '크루 공지를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    languages = models.ManyToManyField(
        Language,
        related_name='crews',
        help_text=(
            '유저가 사용 가능한 언어를 입력해주세요.'
        ),
    )
    max_member = models.IntegerField(
        help_text=(
            '크루 최대 인원을 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 최대 인원 제한
        ],
    )
    is_boj_user_only = models.BooleanField(
        help_text=(
            '백준 아이디 필요 여부를 입력해주세요.'
        ),
        default=False,
    )
    min_boj_tier = models.IntegerField(
        help_text=(
            '최소 백준 레벨을 입력해주세요. ',
            '0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I'
        ),
        choices=BOJLevel.choices,
        blank=True,
        null=True,
        default=None,
    )
    max_boj_tier = models.IntegerField(
        help_text=(
            '최대 백준 레벨을 입력해주세요. ',
            '0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I'
        ),
        validators=[
            # TODO: 최대 레벨이 최소 레벨보다 높은지 검사
        ],
        choices=BOJLevel.choices,
        blank=True,
        null=True,
        default=None,
    )
    tags = models.JSONField(
        help_text=(
            '태그를 입력해주세요.'
        ),
        validators=[
            # TODO: 태그 형식 검사
        ],
        blank=True,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f'[{self.emoji} {self.name}]'

    def __str__(self) -> str:
        member_count = f'({self.members.count()}/{self.max_member})'
        return f'{self.pk} : {self.__repr__()} {member_count} ← {self.captain.__repr__()}'
