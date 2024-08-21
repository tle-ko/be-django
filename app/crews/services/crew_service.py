from typing import List
from typing import Iterable

from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework import exceptions

from crews import dto
from crews import enums
from crews import models
from crews.services.crew_activity_service import CrewActivityService
from problems.models import Problem
from problems.services import ProblemService
from users.models import User
from users.models import UserBojLevelChoices


class CrewService:
    @staticmethod
    def create(languages: List[str] = [], **fields) -> models.Crew:
        with atomic():
            crew = models.Crew.objects.create(**fields)
            service = CrewService(crew)
            service.save_languages(languages)

    @staticmethod
    def query_as_member(user: User) -> QuerySet[models.Crew]:
        """자신이 멤버로 있는 크루를 조회하는 쿼리를 반환"""
        # TODO: Query 최적화 필요
        crew_ids = CrewService._crew_ids_as_member(user)
        return models.Crew.objects.filter(pk__in=crew_ids)

    @staticmethod
    def query_recruiting(user: User) -> QuerySet[models.Crew]:
        """자신이 멤버로 있지 않으면서 크루원을 모집중인 크루를 조회하는 쿼리를 반환"""
        crew_ids = CrewService._crew_ids_as_member(user)
        return models.Crew.objects.filter(**{
            models.Crew.field_name.IS_RECRUITING: True,
        }).exclude(pk__in=crew_ids)

    @staticmethod
    def _crew_ids_as_member(user: User) -> List[int]:
        if not user.is_authenticated:
            return []
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.USER: user,
        }).values_list(models.CrewMember.field_name.CREW)

    def __init__(self, instance: models.Crew) -> None:
        assert isinstance(instance, models.Crew)
        self.instance = instance

    def query_members(self) -> QuerySet[models.CrewMember]:
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: self.instance,
        })

    def query_languages(self) -> QuerySet[models.CrewSubmittableLanguage]:
        return models.CrewSubmittableLanguage.objects.filter(**{
            models.CrewSubmittableLanguage.field_name.CREW: self.instance,
        })

    def query_activities(self) -> QuerySet[models.CrewActivity]:
        return CrewActivityService.query_all(self.instance)

    def statistics(self) -> dto.ProblemStatistic:
        stat = dto.ProblemStatistic()
        for problem in self.problems():
            service = ProblemService(problem)
            for tag in service.tags():
                problem_tag = dto.ProblemTag(
                    key=tag.key,
                    name_ko=tag.name_ko,
                    name_en=tag.name_en,
                )
                stat.tags[problem_tag] += 1
            stat.difficulty[service.difficulty()] += 1
            stat.sample_count += 1
        return stat

    def activities(self) -> List[dto.CrewActivity]:
        activities = []
        queryset = CrewActivityService.query_all(self.instance)
        for nth, entity in enumerate(queryset, start=1):
            service = CrewActivityService(entity)
            # TODO: 회차 이름을 모델 생성과 함께 고정
            activities.append(dto.CrewActivity(
                activity_id=service.instance.pk,
                name=f'{nth}회차',
                start_at=service.instance.start_at,
                end_at=service.instance.end_at,
                is_in_progress=service.is_in_progress(),
                has_started=service.has_started(),
                has_ended=service.has_ended(),
            ))
        return activities

    def captain(self) -> models.CrewMember:
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: self.instance,
            models.CrewMember.field_name.IS_CAPTAIN: True,
        })

    def problems(self) -> List[Problem]:
        return models.CrewActivityProblem.objects.filter(**{
            models.CrewActivityProblem.field_name.CREW: self.instance,
        }).values_list(models.CrewActivityProblem.field_name.PROBLEM, flat=True)

    def languages(self) -> List[enums.ProgrammingLanguageChoices]:
        languages = []
        for submittable_language in self.query_languages():
            language = enums.ProgrammingLanguageChoices(submittable_language.language)
            languages.append(language)
        return languages

    def save_languages(self, languages: List[enums.ProgrammingLanguageChoices]) -> List[models.CrewSubmittableLanguage]:
        assert isinstance(languages, list)
        self.delete_languages()
        entities = []
        for language in languages:
            self._validate_language(language)
            entity = models.CrewSubmittableLanguage(**{
                models.CrewSubmittableLanguage.field_name.CREW: self.instance,
                models.CrewSubmittableLanguage.field_name.LANGUAGE: language,
            })
            entities.append(entity)
        return models.CrewSubmittableLanguage.objects.bulk_create(entities)

    def _validate_language(self, language: str):
        assert isinstance(language, str) or isinstance(
            language, enums.ProgrammingLanguageChoices)
        if language not in enums.ProgrammingLanguageChoices:
            raise exceptions.ValidationError(f'{language}은 선택 가능한 언어가 아닙니다.')

    def delete_languages(self):
        self.query_languages().delete()

    def min_boj_level(self) -> UserBojLevelChoices:
        if self.instance.min_boj_level is None:
            return UserBojLevelChoices.U
        return UserBojLevelChoices(self.instance.min_boj_level)

    def is_captain(self, user: User) -> bool:
        assert isinstance(user, User)
        return self.captain().user == user

    def is_member(self, user: User) -> bool:
        assert isinstance(user, User)
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: self.instance,
            models.CrewMember.field_name.USER: user,
        }).exists()

    def validate_applicant(self, applicant: User, raises_exception=False) -> bool:
        assert isinstance(applicant, User)
        try:
            self._validate_applicant_boj_level(applicant)
        except exceptions.ValidationError as exception:
            if not raises_exception:
                return False
            raise exception
        return True

    def _validate_applicant(self, applicant: User):
        if not self.instance.is_recruiting:
            raise exceptions.ValidationError('크루가 현재 크루원을 모집하고 있지 않습니다.')
        if self.query_members().count() >= self.instance.max_members:
            raise exceptions.ValidationError('크루의 최대 정원을 초과하였습니다.')
        if self.is_member(applicant):
            raise exceptions.ValidationError('이미 가입한 크루입니다.')
        self._validate_applicant_boj_level(applicant)

    def validate_applicant_boj_level(self, applicant: User, raises_exception=False) -> bool:
        assert isinstance(applicant, User)
        try:
            self._validate_applicant_boj_level(applicant)
        except exceptions.ValidationError as exception:
            if not raises_exception:
                return False
            raise exception
        return True

    def _validate_applicant_boj_level(self, applicant: User):
        if self.instance.min_boj_level is None:
            return
        if applicant.boj_level is None:
            raise exceptions.ValidationError('사용자의 백준 레벨을 가져올 수 없습니다.')
        if applicant.boj_level < self.instance.min_boj_level:
            raise exceptions.ValidationError('최소 백준 레벨 요구조건을 달성하지 못하였습니다.')

    def tags(self) -> List[dto.CrewTag]:
        # 태그의 나열 순서는 리스트에 선언한 순서를 따름.
        return [
            *self._get_language_tags(),
            *self._get_min_level_tags(),
            *self._get_custom_tags(),
        ]

    def _get_language_tags(self) -> Iterable[dto.CrewTag]:
        for language in self.languages():
            yield dto.CrewTag(
                key=language.value,
                name=language.label,
                type=enums.CrewTagType.LANGUAGE,
            )

    def _get_min_level_tags(self) -> Iterable[dto.CrewTag]:
        yield dto.CrewTag(
            key=None,
            name=self._get_min_level_tag_name(),
            type=enums.CrewTagType.LEVEL,
        )

    def _get_min_level_tag_name(self) -> str:
        min_level = self.min_boj_level()
        if min_level == UserBojLevelChoices.U:
            return '티어 무관'
        elif min_level.get_tier() == 5:
            return f"{min_level.get_division_name(lang='ko')} 이상"
        else:
            return f"{min_level.get_name(lang='ko', arabic=False)} 이상"

    def _get_custom_tags(self) -> Iterable[dto.CrewTag]:
        for tag in self.instance.custom_tags:
            yield dto.CrewTag(
                key=None,
                name=tag,
                type=enums.CrewTagType.CUSTOM,
            )
