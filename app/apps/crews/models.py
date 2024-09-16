from __future__ import annotations

from typing import List
from typing import Union

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AnonymousUser

from apps.boj.enums import BOJLevel
from apps.crews import dto
from apps.crews import enums
from users.models import User


class CrewManager(models.Manager):
    def filter(self,
               as_captain: User = None,
               as_member: User = None,
               not_as_member: User = None,
               is_recruiting: bool = None,
               *args,
               **kwargs) -> models.QuerySet[Crew]:
        if is_recruiting is not None:
            kwargs[Crew.field_name.IS_RECRUITING] = is_recruiting
        queryset = super().filter(*args, **kwargs)
        if as_captain is not None:
            assert isinstance(as_captain, User)
            queryset = queryset.filter(pk__in=self._ids_as_captain(as_captain))
        if as_member is not None:
            assert isinstance(as_member, User)
            queryset = queryset.filter(pk__in=self._ids_as_member(as_member))
        if not_as_member is not None and not isinstance(not_as_member, AnonymousUser):
            assert isinstance(not_as_member, User)
            queryset = queryset.exclude(
                pk__in=self._ids_as_member(not_as_member),
            )
        return queryset

    def _ids_as_captain(self, user: User) -> List[int]:
        return CrewMember.objects.filter(user=user, is_captain=True).values_list(CrewMember.field_name.CREW, flat=True)

    def _ids_as_member(self, user: User) -> List[int]:
        return CrewMember.objects.filter(user=user).values_list(CrewMember.field_name.CREW, flat=True)


class Crew(models.Model):
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

    objects: CrewManager = CrewManager()

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

    def display_name(self) -> str:
        return f'{self.icon} {self.name}'

    def tags(self) -> List[dto.CrewTagDTO]:
        tags = []
        # 사용 가능 언어
        for language_value in CrewSubmittableLanguage.objects.filter(crew=self).values_list(CrewSubmittableLanguage.field_name.LANGUAGE, flat=True):
            language = enums.ProgrammingLanguageChoices(language_value)
            tag_dto = dto.CrewTagDTO(
                key=language.value,
                name=language.label,
                type=enums.CrewTagType.LANGUAGE,
            )
            tags.append(tag_dto)
        # 백준 최소 요구 티어
        min_level = BOJLevel(self.min_boj_level)
        if min_level == BOJLevel.U:
            tag_name = '티어 무관'
        elif min_level.get_tier() == 5:
            tag_name = f"{min_level.get_division_name(lang='ko')} 이상"
        else:
            tag_name = f"{min_level.get_name(lang='ko', arabic=False)} 이상"
        tag_dto = dto.CrewTagDTO(
            key=None,
            name=tag_name,
            type=enums.CrewTagType.LEVEL,
        )
        tags.append(tag_dto)
        # 커스텀 태그
        for tag_name in self.custom_tags:
            tag_dto = dto.CrewTagDTO(
                key=None,
                name=tag_name,
                type=enums.CrewTagType.CUSTOM,
            )
            tags.append(tag_dto)
        return tags

    def save(self, *args, **kwargs) -> None:
        retval = super().save(*args, **kwargs)
        if not CrewMember.objects.filter(crew=self, is_captain=True).exists():
            # 크루 생성 시 선장을 자동으로 생성합니다.
            CrewMember.objects.create(**{
                CrewMember.field_name.CREW: self,
                CrewMember.field_name.USER: self.created_by,
                CrewMember.field_name.IS_CAPTAIN: True,
            })
        return retval


class CrewMemberManager(models.Manager):
    def filter(self,
               user: User = None,
               crew: Crew = None,
               is_captain: bool = None,
               *args, **kwargs) -> models.QuerySet[CrewMember]:
        if user is not None:
            kwargs[CrewMember.field_name.USER] = user
        if crew is not None:
            kwargs[CrewMember.field_name.CREW] = crew
        if is_captain is not None:
            kwargs[CrewMember.field_name.IS_CAPTAIN] = is_captain
        return super().filter(*args, **kwargs)

    def get_captain(self, crew: Crew) -> CrewMember:
        return self.filter(crew=crew, is_captain=True).get()


class CrewMember(models.Model):
    crew = models.ForeignKey(
        Crew,
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

    objects: _CrewMemberManager = CrewMemberManager()

    class field_name:
        CREW = 'crew'
        USER = 'user'
        IS_CAPTAIN = 'is_captain'
        CREATED_AT = 'created_at'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : "{self.user.username}"@"{self.crew.display_name()}"]'


class CrewSubmittableLanguageManager(models.Manager):
    def filter(self,
               crew: Crew = None,
               *args,
               **kwargs) -> models.QuerySet[CrewSubmittableLanguage]:
        if crew is not None:
            kwargs[CrewSubmittableLanguage.field_name.CREW] = crew
        return super().filter(*args, **kwargs)

    def bulk_create_from_languages(self, crew: Crew, languages: List[Union[str, enums.ProgrammingLanguageChoices]]) -> List[CrewSubmittableLanguage]:
        assert isinstance(crew, Crew)
        entities = []
        for language in languages:
            if isinstance(language, str):
                language = enums.ProgrammingLanguageChoices(language)
            elif isinstance(language, enums.ProgrammingLanguageChoices):
                pass
            else:
                raise ValueError(f'{language}은 선택 가능한 언어가 아닙니다.')
            entity = CrewSubmittableLanguage(**{
                CrewSubmittableLanguage.field_name.CREW: crew,
                CrewSubmittableLanguage.field_name.LANGUAGE: language,
            })
            entities.append(entity)
        return CrewSubmittableLanguage.objects.bulk_create(entities)


class CrewSubmittableLanguage(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
    )
    language = models.TextField(
        choices=enums.ProgrammingLanguageChoices.choices,
        help_text='언어 키를 입력해주세요. (최대 20자)',
    )

    objects: _CrewSubmittableLanguageManager = CrewSubmittableLanguageManager()

    class field_name:
        CREW = 'crew'
        LANGUAGE = 'language'

    class Meta:
        ordering = ['crew']

    def __str__(self) -> str:
        return f'[{self.pk} : #{self.language}]'


_CrewMemberManager = Union[CrewMemberManager, models.Manager[CrewMember]]
_CrewSubmittableLanguageManager = Union[CrewSubmittableLanguageManager,
                                        models.Manager[CrewSubmittableLanguage]]
