from __future__ import annotations

from typing import List
from typing import Union

from django.contrib.auth.models import AnonymousUser
from django.db.models import Manager
from django.db.models import QuerySet

from apps.boj.enums import BOJLevel
from apps.activities.models import CrewActivity
from apps.activities.models import CrewActivityProblem
from apps.problems.dto import ProblemStatisticDTO
from apps.problems.statistics import create_statistics
from users.models import User

from . import db
from . import dto
from . import enums


class CrewQuerySet(QuerySet):
    def exclude(self,
                as_captain: User = None,
                as_member: User = None,
                is_recruiting: bool = None,
                *args,
                **kwargs) -> CrewQuerySet:
        return self._kwargs_filtering(super().exclude, as_captain, as_member, is_recruiting, *args, **kwargs)

    def filter(self,
               as_captain: User = None,
               as_member: User = None,
               is_recruiting: bool = None,
               *args,
               **kwargs) -> CrewQuerySet:
        return self._kwargs_filtering(super().filter, as_captain, as_member, is_recruiting, *args, **kwargs)

    def is_recruiting(self, user: User) -> CrewQuerySet:
        return self.filter(is_recruiting=True).exclude(as_member=user)

    def as_member(self, user: User) -> CrewQuerySet:
        return self.filter(as_member=user).order_by(
            '-'+Crew.field_name.UPDATED_AT,
            '-'+Crew.field_name.IS_ACTIVE,
        )

    def _kwargs_filtering(self,
                          filter_function,
                          as_captain: User = None,
                          as_member: User = None,
                          is_recruiting: bool = None,
                          **kwargs) -> CrewQuerySet:
        if is_recruiting is not None:
            kwargs[Crew.field_name.IS_RECRUITING] = is_recruiting
        if as_captain is not None:
            assert bool(
                isinstance(as_captain, User)
                or
                isinstance(as_captain, AnonymousUser)
            )
            kwargs['pk__in'] = self._ids_as_captain(as_captain)
        if as_member is not None:
            assert bool(
                isinstance(as_member, User)
                or
                isinstance(as_member, AnonymousUser)
            )
            kwargs['pk__in'] = self._ids_as_member(as_member)
        return filter_function(**kwargs)

    def _ids_as_captain(self, user: User) -> List[int]:
        if not user.is_authenticated:
            return []
        else:
            return CrewMember.objects.filter(user=user, is_captain=True).values_list(CrewMember.field_name.CREW, flat=True)

    def _ids_as_member(self, user: User) -> List[int]:
        if not user.is_authenticated:
            return []
        else:
            return CrewMember.objects.filter(user=user).values_list(CrewMember.field_name.CREW, flat=True)


class CrewManager(Manager):
    def get_queryset(self) -> QuerySet:
        return CrewQuerySet(self.model, using=self._db)


class Crew(db.CrewDAO):
    objects: CrewQuerySet = CrewManager.from_queryset(CrewQuerySet)()

    class Meta:
        proxy = True

    def activities(self) -> List[dto.CrewActivityDTO]:
        return [obj.as_dto() for obj in CrewActivity.objects.filter(crew=self)]

    def latest_activity(self) -> dto.CrewActivityDTO:
        if not self.is_active:
            return dto.CrewActivityDTO.none('활동 종료')
        try:
            obj = CrewActivity.objects.filter(crew=self).latest()
        except CrewActivity.DoesNotExist:
            return dto.CrewActivityDTO.none('등록된 활동 없음')
        else:
            return obj.as_dto()

    def as_dto(self) -> dto.CrewDTO:
        return dto.CrewDTO(
            crew_id=self.pk,
            name=self.name,
            icon=self.icon,
            is_active=self.is_active,
            latest_activity=self.latest_activity(),
        )

    def captain(self) -> CrewMember:
        return CrewMember.objects.get_captain(self)

    def dashboard(self, user: User) -> dto.CrewDashboardDTO:
        return dto.CrewDashboardDTO(
            **self.as_dto().__dict__,
            notice=self.notice,
            tags=self.tags(),
            members=self.members(),
            activities=self.activities(),
            is_captain=self.is_captain(user),
        )

    def display_name(self) -> str:
        return f'{self.icon} {self.name}'

    def is_captain(self, user: User) -> bool:
        return CrewMember.objects.filter(crew=self, user=user, is_captain=True).exists()

    def members(self) -> List[dto.CrewMemberDTO]:
        return [obj.as_dto() for obj in CrewMember.objects.filter(crew=self)]

    def statistics(self) -> ProblemStatisticDTO:
        queryset = CrewActivityProblem.objects.filter(crew=self)
        return create_statistics(obj.problem for obj in queryset)

    def tags(self) -> List[dto.CrewTagDTO]:
        return self.tags__language() + self.tags__level() + self.tags__custom()

    def tags__language(self) -> List[dto.CrewTagDTO]:
        # 사용 가능 언어
        return [obj.as_tag_dto() for obj in CrewSubmittableLanguage.objects.filter(crew=self)]

    def tags__level(self) -> List[dto.CrewTagDTO]:
        # 백준 최소 요구 티어
        min_level = BOJLevel(self.min_boj_level)
        if min_level == BOJLevel.U:
            tag_name = '티어 무관'
        elif min_level.get_tier() == 5:
            tag_name = f"{min_level.get_division_name(lang='ko')} 이상"
        else:
            tag_name = f"{min_level.get_name(lang='ko', arabic=False)} 이상"
        return [
            dto.CrewTagDTO(
                key=None,
                name=tag_name,
                type=enums.CrewTagType.LEVEL,
            ),
        ]

    def tags__custom(self) -> List[dto.CrewTagDTO]:
        # 커스텀 태그
        return [
            dto.CrewTagDTO(
                key=None,
                name=tag_name,
                type=enums.CrewTagType.CUSTOM,
            )
            for tag_name in self.custom_tags
        ]


class CrewMemberManager(Manager):
    def filter(self,
               user: User = None,
               crew: Crew = None,
               is_captain: bool = None,
               *args, **kwargs) -> QuerySet[CrewMember]:
        if user is not None:
            kwargs[CrewMember.field_name.USER] = user
        if crew is not None:
            kwargs[CrewMember.field_name.CREW] = crew
        if is_captain is not None:
            kwargs[CrewMember.field_name.IS_CAPTAIN] = is_captain
        return super().filter(*args, **kwargs)

    def get_captain(self, crew: Crew) -> CrewMember:
        return self.filter(crew=crew, is_captain=True).get()


class CrewMember(db.CrewMemberDAO):
    objects: CrewMemberManager = CrewMemberManager()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.CrewMemberDTO:
        return dto.CrewMemberDTO(
            **self.user.as_dto().__dict__,
            is_captain=self.is_captain,
        )


class CrewSubmittableLanguageManager(Manager):
    def filter(self,
               crew: Crew = None,
               *args,
               **kwargs) -> QuerySet[CrewSubmittableLanguage]:
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


class CrewSubmittableLanguage(db.CrewSubmittableLanguageDAO):
    objects: CrewSubmittableLanguageManager = CrewSubmittableLanguageManager()

    class Meta:
        proxy = True

    def as_tag_dto(self) -> dto.CrewTagDTO:
        language = enums.ProgrammingLanguageChoices(self.language)
        return dto.CrewTagDTO(
            key=language.value,
            name=language.label,
            type=enums.CrewTagType.LANGUAGE,
        )
