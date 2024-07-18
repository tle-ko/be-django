from __future__ import annotations
import typing

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from tle.models.user_solved_tier import UserSolvedTier
from tle.models.submission_language import SubmissionLanguage


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='크루 이름을 입력해주세요. (최대 20자)',
    )
    emoji = models.CharField(
        max_length=2,
        validators=[
            # TODO: 이모지 형식 검사
        ],
        null=True,
        blank=True,
        help_text='크루 아이콘을 입력해주세요. (이모지)',
    )
    max_members = models.IntegerField(
        help_text='크루 최대 인원을 입력해주세요.',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ],
        default=8,
        blank=False,
        null=False,
    )
    notice = models.TextField(
        help_text='크루 공지를 입력해주세요.',
        null=True,
        blank=True,
        max_length=500,  # TODO: 최대 길이 제한이 적정한지 검토
    )
    is_boj_user_only = models.BooleanField(
        help_text='백준 아이디 필요 여부를 입력해주세요.',
        default=False,
    )
    min_boj_tier = models.IntegerField(
        help_text='최소 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
        choices=UserSolvedTier.choices,
        blank=True,
        null=True,
        default=None,
    )
    max_boj_tier = models.IntegerField(
        help_text='최대 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
        validators=[
            # TODO: 최대 레벨이 최소 레벨보다 높은지 검사
        ],
        choices=UserSolvedTier.choices,
        blank=True,
        null=True,
        default=None,
    )
    allowed_languages = models.ManyToManyField(
        SubmissionLanguage,
        related_name='crews',
        help_text='유저가 사용 가능한 언어를 입력해주세요.',
    )
    custom_tags = models.JSONField(
        help_text='태그를 입력해주세요.',
        validators=[
            # TODO: 태그 형식 검사
        ],
        blank=True,
        default=list,
    )
    is_recruiting = models.BooleanField(
        help_text='모집 중 여부를 입력해주세요.',
        default=True,
    )
    is_active = models.BooleanField(
        help_text='활동 중인지 여부를 입력해주세요.',
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def captain(self) -> T_CrewMember:
        return self.members.get(is_captain=True)

    class FieldName:
        APPLICANTS = 'applicants'
        MEMBERS = 'members'

    if typing.TYPE_CHECKING:
        from . import (
            CrewApplicant as T_CrewApplicant,
            CrewMember as T_CrewMember,
        )
        applicants: models.ManyToManyField[T_CrewApplicant]
        members: models.ManyToManyField[T_CrewMember]

    def __repr__(self) -> str:
        return f'[{self.emoji} {self.name}]'

    def __str__(self) -> str:
        member_count = f'({self.members.count()}/{self.max_member})'
        return f'{self.pk} : {self.__repr__()} {member_count} ← {self.captain.__repr__()}'
