from __future__ import annotations

from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from apps.boj.enums import BOJLevel
from users.models import User

from . import enums


class CrewDAO(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='크루 이름을 입력해주세요. (최대 20자)',
    )
    icon = models.TextField(
        choices=enums.EmojiChoices.choices,
        null=False,
        blank=False,
        default=enums.EmojiChoices.U1F6A2,  # :ship:
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
        choices=BOJLevel.choices,
        default=BOJLevel.U,
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
        PK = 'pk'
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

    class method_name:
        GET_DISPLAY_NAME = 'get_display_name'

    class Meta:
        verbose_name = 'Crew'
        verbose_name_plural = 'Crews'
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.icon} "{self.name}"]'

    def save(self, *args, **kwargs):
        retval = super().save(*args, **kwargs)
        if not CrewMemberDAO.objects.filter(crew=self, is_captain=True).exists():
            # 크루 생성 시 선장을 자동으로 생성합니다.
            CrewMemberDAO.objects.create(**{
                CrewMemberDAO.field_name.CREW: self,
                CrewMemberDAO.field_name.USER: self.created_by,
                CrewMemberDAO.field_name.IS_CAPTAIN: True,
            })
        return retval

    @admin.display(description='Display Name')
    def get_display_name(self) -> str:
        return f'{self.icon} {self.name}'


class CrewMemberDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='유저를 입력해주세요.',
    )
    is_captain = models.BooleanField(
        default=False,
        help_text='크루장 여부',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        PK = 'pk'
        CREW = 'crew'
        USER = 'user'
        IS_CAPTAIN = 'is_captain'
        CREATED_AT = 'created_at'

    class Meta:
        verbose_name = 'Crew Member'
        verbose_name_plural = 'Crew Members'
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : "{self.user.username}"@"{self.crew}"]'


class CrewSubmittableLanguageDAO(models.Model):
    crew = models.ForeignKey(
        CrewDAO,
        on_delete=models.CASCADE,
    )
    language = models.TextField(
        choices=enums.ProgrammingLanguageChoices.choices,
        help_text='언어 키를 입력해주세요. (최대 20자)',
    )

    class field_name:
        PK = 'pk'
        CREW = 'crew'
        LANGUAGE = 'language'

    class Meta:
        verbose_name = 'Crew Submittable Language'
        verbose_name_plural = 'Crew Submittable Languages'
        ordering = ['crew']

    def __str__(self) -> str:
        return f'[{self.pk} : #{self.language}]'
