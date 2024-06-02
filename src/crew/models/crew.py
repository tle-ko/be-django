from django.core.validators import MinValueValidator
from django.db import models

from user.models import User
from boj.models import BOJLevel


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '크루 이름을 입력해주세요. (최대 20자)'
        ),
    )
    emoji = models.CharField(
        max_length=1,
        help_text=(
            '크루 아이콘을 입력해주세요. (이모지)'
        ),
        null=True,
        blank=True,
    )
    captain = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='crews',
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CrewMemeber(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='members',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='crews',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    is_approved = models.BooleanField(
        help_text=(
            '가입 승인 여부를 입력해주세요.'
        ),
        default=False,
    )
    approved_at = models.DateTimeField(
        help_text=(
            '가입 승인 일자를 입력해주세요.'
        ),
        null=True,
        default=None,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class CrewRecruitment(models.Model):
    crew = models.OneToOneField(
        Crew,
        on_delete=models.CASCADE,
        related_name='opening',
        help_text=(
            '크루를 입력해주세요.'
        ),
        unique=True,
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
    tags = models.JSONField(
        help_text=(
            '태그를 입력해주세요.'
        ),
        validators=[
            # TODO: 태그 형식 검사
        ],
    )
    allowed_languages = models.JSONField(
        help_text=(
            '허용 언어를 입력해주세요. ',
            '언어의 아이디를 입력해주세요.'
        ),
        validators=[
            # TODO: 언어 아이디 검사
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
        default=BOJLevel.U,
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
        default=BOJLevel.R1,
    )
