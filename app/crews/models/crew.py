from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from crews.validators import EmojiValidator
from users.models import User, UserBojLevelChoices


class Crew(models.Model):
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
        choices=UserBojLevelChoices.choices,
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

    def __str__(self) -> str:
        return f'[{self.pk} : {self.icon} "{self.name}"]'
