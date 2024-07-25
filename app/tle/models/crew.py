from __future__ import annotations
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

if typing.TYPE_CHECKING:
    import tle.models as _T


class EmojiValidator(BaseValidator):
    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __call__(self, value) -> None:
        try:
            Emoji(value)  # just checking if it's valid emoji
        except ValueError:
            raise ValidationError(self.message, params={"value": value})


class Crew(models.Model):
    if typing.TYPE_CHECKING:
        applicants: models.ManyToManyField[_T.CrewApplicant]
        members: models.ManyToManyField[_T.CrewMember]
        activities: models.ManyToManyField[_T.CrewActivity]
        submittable_languages: models.ManyToManyField[SubmissionLanguage]

    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='크루 이름을 입력해주세요. (최대 20자)',
    )
    icon = models.CharField(
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
    min_boj_level = models.IntegerField(
        help_text='최소 백준 레벨을 입력해주세요. 0: Unranked, 1: Bronze V, 2: Bronze IV, ..., 6: Silver V, ..., 30: Ruby I',
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

    class field_name:
        # related fields
        APPLICANTS = 'applicants'
        MEMBERS = 'members'
        ACTIVITIES = 'activities'
        SUBMITTABLE_LANGUAGES = 'submittable_languages'
        # fields
        NAME = 'name'
        ICON = 'icon'
        MAX_MEMBERS = 'max_members'
        NOTICE = 'notice'
        CUSTOM_TAGS = 'custom_tags'
        MIN_BOJ_LEVEL = 'min_boj_level'
        IS_RECRUITING = 'is_recruiting'
        IS_ACTIVE = 'is_active'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['-updated_at']

    @classmethod
    def of_user(cls, user: User) -> models.QuerySet[Crew]:
        return cls.objects.filter(members__user=user)

    @classmethod
    def of_user_as_captain(cls, user: User) -> models.QuerySet[Crew]:
        return cls.objects.filter(created_by=user)

    def __str__(self) -> str:
        return f'[{self.pk} : {self.icon} "{self.name}"] ({self.members.count()}/{self.max_members})'

    def save(self, *args, **kwargs) -> None:
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.set_captain(self.created_by)

    def get_display_name(self) -> str:
        return f'{self.icon} {self.name}'

    def get_captain(self) -> User:
        return self.members.get(is_captain=True).user

    def set_captain(self, user: User) -> None:
        assert isinstance(user, User)
        with transaction.atomic():
            self.members.filter(is_captain=True).update(is_captain=False)
            try:
                captain = self.members.get(user=user)
                captain.is_captain = True
            except self.members.model.DoesNotExist:
                captain = self.members.create(user=user, is_captain=True)
            finally:
                captain.save()

    def is_captain(self, user: User) -> bool:
        return self.members.filter(user=user, is_captain=True).exists()

    def is_member(self, user: User) -> bool:
        return self.members.filter(user=user).exists()

    def is_joinable(self, user: User) -> bool:
        if not self.is_recruiting:
            return False
        if self.members.count() >= self.max_members:
            return False
        if self.is_member(user):
            return False
        if self.min_boj_level is not None:
            return bool(
                (user.boj_level is not None) and
                (user.boj_level >= self.min_boj_level)
            )
        return True
