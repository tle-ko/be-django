from typing import Iterable
from typing import List
from typing import Optional

from django.db.models import QuerySet
from django.utils import timezone

from crews import dto
from crews import enums
from crews import models
from problems.models import ProblemAnalysis
from problems.models import ProblemDifficultyChoices
from users.models import User
from users.models import UserBojLevelChoices


def problem_statistics(crew: models.Crew) -> dto.ProblemStatistic:
    assert isinstance(crew, models.Crew)
    statistics = dto.ProblemStatistic()
    queryset = models.CrewActivityProblem.objects.filter(**{
        models.CrewActivityProblem.field_name.CREW: crew,
    })
    for activity_problem in queryset:
        statistics.sample_count += 1
        try:
            analysis = ProblemAnalysis.objects.filter(**{
                ProblemAnalysis.field_name.PROBLEM: activity_problem.problem,
            }).latest()
        except ProblemAnalysis.DoesNotExist:
            statistics.difficulty[ProblemDifficultyChoices.UNDER_ANALYSIS.value] += 1
        else:
            statistics.difficulty[analysis.difficulty] += 1
            for tag in analysis.tags:
                problem_tag = dto.ProblemTag(
                    key=tag.key,
                    name_ko=tag.name_ko,
                    name_en=tag.name_en,
                )
                statistics.tags[problem_tag] += 1
    return statistics


def crew_of_user_queryset(include_user: Optional[User] = None,
                          exclude_user: Optional[User] = None) -> QuerySet[models.Crew]:
    """특정 사용자가 속하거나 속하지 않은 크루 목록을 조회하는 쿼리를 반환한다."""
    queryset = models.Crew.objects
    if include_user is not None:
        queryset = queryset.filter(pk__in=models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.USER: include_user,
        }).values_list(models.CrewMember.field_name.CREW))
    if exclude_user is not None:
        queryset = queryset.exclude(pk__in=models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.USER: exclude_user,
        }).values_list(models.CrewMember.field_name.CREW))
    return queryset


def crew_activities_queryset(crew: models.Crew, exclude_future=True) -> QuerySet[models.CrewActivity]:
    """
    exclude_future: 아직 공개되지 않은 활동도 포함할 지 여부.
    """
    kwargs = {
        models.CrewActivity.field_name.CREW: crew,
    }
    if exclude_future:
        kwargs[models.CrewActivity.field_name.START_AT + '__lte'] = timezone.now()
    return models.CrewActivity.objects.filter(**kwargs).order_by(models.CrewActivity.field_name.START_AT)


def crew_tags(crew: models.Crew) -> List[dto.CrewTag]:
    # 태그의 나열 순서는 리스트에 선언한 순서를 따름.
    return [
        *_get_language_tags(crew),
        *_get_level_tags(crew),
        *_get_custom_tags(crew),
    ]


def _get_language_tags(crew: models.Crew) -> Iterable[dto.CrewTag]:
    submittable_languages = models.CrewSubmittableLanguage.objects.filter(**{
        models.CrewSubmittableLanguage.field_name.CREW: crew,
    })
    for submittable_language in submittable_languages.all():
        programming_language = models.ProgrammingLanguageChoices(submittable_language)
        yield dto.CrewTag(
            key=programming_language.key,
            name=programming_language.name,
            type=enums.CrewTagType.LANGUAGE,
        )


def _get_level_tags(crew: models.Crew) -> Iterable[dto.CrewTag]:
    yield dto.CrewTag(
        key=None,
        name=_get_bounded_level_name(UserBojLevelChoices(crew.min_boj_level)),
        type=dto.CrewTagType.LEVEL,
    )


def _get_custom_tags(crew: models.Crew) -> Iterable[dto.CrewTag]:
    for tag in crew.custom_tags:
        yield dto.CrewTag(
            key=None,
            name=tag,
            type=dto.CrewTagType.CUSTOM,
        )


def _get_bounded_level_name(level: Optional[UserBojLevelChoices],
                            bound_tier: int = 5,
                            bound_msg: str = "이상",
                            default_msg: str = "티어 무관",
                            lang='ko',
                            arabic=False) -> str:
    """level에 대한 백준 난이도 태그 이름을 반환한다.

    bound_tier는 해당 랭크(브론즈,실버,...)를 모두 아우르는 마지막
    티어(1,2,3,4,5)를 의미한다.

    bound_msg는 "이상", 혹은 "이하"를 나타내는 제한 메시지이다.

    만약 level의 티어가 bound_tier와
    같다면 랭크만 출력하고,
    같지않다면 랭크와 티어 모두 출력한다.

    메시지의 마지막에는 bound_msg를 출력한다.
    """
    if level is None:
        return default_msg
    assert isinstance(level, UserBojLevelChoices)
    if level.get_tier() == bound_tier:
        return f'{level.get_division_name(lang=lang)} {bound_msg}'
    else:
        return f'{level.get_name(lang=lang, arabic=arabic)} {bound_msg}'


def crew_member_count(crew: models.Crew) -> int:
    return models.CrewMember.objects.filter(**{
        models.CrewMember.field_name.CREW: crew,
    }).count()


def crew_is_joinable(crew: models.Crew, user: User) -> bool:
    if not crew.is_recruiting:
        return False
    if crew_member_count(crew) >= crew.max_members:
        return False
    if crew_is_member(crew, user):
        return False
    if crew.min_boj_level is not None:
        return bool(
            (user.boj_level is not None) and
            (user.boj_level >= crew.min_boj_level)
        )
    return True


def crew_is_member(crew: models.Crew, user: User) -> bool:
    return models.CrewMember.objects.filter(**{
        models.CrewMember.field_name.CREW: crew,
        models.CrewMember.field_name.USER: user,
    }).exists()
