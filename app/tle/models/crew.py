from __future__ import annotations
import dataclasses
import typing

from django.core.exceptions import ValidationError
from django.core.validators import (
    BaseValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models, transaction

from tle.enums import Emoji
from tle.models.choices import BojUserLevel
from tle.models.user import User
from tle.models.submission_language import SubmissionLanguage


class EmojiValidator(BaseValidator):
    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __call__(self, value) -> None:
        try:
            Emoji(value) # just checking if it's valid emoji
        except ValueError:
            raise ValidationError(self.message, params={"value": value})


@dataclasses.dataclass
class CrewTag:
    key: typing.Optional[str]
    name: str

    @classmethod
    def from_language(cls, lang: SubmissionLanguage) -> CrewTag:
        return CrewTag(key=lang.key, name=lang.name)

    @classmethod
    def from_name(cls, name: str) -> CrewTag:
        return CrewTag(key=None, name=name)


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='크루 이름을 입력해주세요. (최대 20자)',
    )
    emoji = models.CharField(
        max_length=2,
        validators=[EmojiValidator(message='이모지 형식이 아닙니다.')],
        null=False,
        blank=False,
        default='🚢',
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
    submittable_languages = models.ManyToManyField(
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
    is_boj_username_required = models.BooleanField(
        help_text='백준 아이디 필요 여부를 입력해주세요.',
        default=False,
    )
    min_boj_level = models.IntegerField(
        help_text='최소 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
        choices=BojUserLevel.choices,
        blank=True,
        null=True,
        default=None,
    )
    max_boj_level = models.IntegerField(
        help_text='최대 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
        validators=[
            # TODO: 최대 레벨이 최소 레벨보다 높은지 검사
        ],
        choices=BojUserLevel.choices,
        blank=True,
        null=True,
        default=None,
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
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
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
        submittable_languages: models.ManyToManyField[SubmissionLanguage]

    def __repr__(self) -> str:
        return f'[{self.emoji} {self.name}]'

    def __str__(self) -> str:
        member_count = f'({self.members.count()}/{self.max_members})'
        return f'{self.pk} : {self.__repr__()} {member_count} ← {self.captain.__repr__()}'

    def save(self, *args, **kwargs) -> None:
        with transaction.atomic():
            obj = super().save(*args, **kwargs)
            if not self.members.filter(user=self.created_by).exists():
                captain = self.members.create(
                    user=self.created_by,
                    is_captain=True
                )
                captain.save()
        return obj

    def is_member(self, user: User) -> bool:
        return self.members.filter(user=user).exists()

    def is_joinable(self, user: User) -> bool:
        if not self.is_recruiting:
            return False
        if self.captain == user:
            return False
        if self.members.count() >= self.max_members:
            return False
        if self.members.filter(user=user).exists():
            return False
        if self.is_boj_username_required:
            if user.boj_username is None:
                # TODO: 인증된 BOJ 사용자명이어야 함
                return False
            if self.min_boj_level is not None:
                if user.boj_level is None:
                    return False
                if user.boj_level < self.min_boj_level:
                    return False
            if self.max_boj_level is not None:
                if user.boj_level is None:
                    return False
                if user.boj_level > self.max_boj_level:
                    return False
        return True

    def get_tags(self) -> typing.List[CrewTag]:
        return [
            *map(CrewTag.from_language, self.submittable_languages.all()),
            *self._build_tier_tags(),
            *map(CrewTag.from_name, self.custom_tags),
        ]

    def _build_tier_tags(self) -> typing.List[CrewTag]:
        tags = []
        if self.min_boj_level is None and self.max_boj_level is None:
            tags.append(CrewTag.from_name('티어 무관'))
        else:
            if self.min_boj_level is not None:
                tags.append(self._build_min_tier_tag())
            if self.max_boj_level is not None:
                tags.append(self._build_max_tier_tag())
        return tags

    def _build_min_tier_tag(self) -> CrewTag:
        if BojUserLevel.get_tier(self.min_boj_level) == 5:
            level_name = BojUserLevel.get_rank_name(self.min_boj_level)
        else:
            level_name = BojUserLevel.get_name(self.min_boj_level)
        return CrewTag.from_name(f'{level_name} 이상')

    def _build_max_tier_tag(self) -> CrewTag:
        if BojUserLevel.get_tier(self.max_boj_level) == 1:
            level_name = BojUserLevel.get_rank_name(self.max_boj_level)
        else:
            level_name = BojUserLevel.get_name(self.max_boj_level)
        return CrewTag.from_name(f'{level_name} 이하')
