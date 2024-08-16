from textwrap import dedent
from typing import Iterable
from typing import List
from typing import Optional

from django.core.mail import send_mail
from django.db.models import QuerySet
from django.db.transaction import atomic
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


class crew:
    @staticmethod
    def of_user_queryset(include_user: Optional[User] = None,
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

    @classmethod
    def tags(cls, crew: models.Crew) -> List[dto.CrewTag]:
        # 태그의 나열 순서는 리스트에 선언한 순서를 따름.
        return [
            *cls._get_language_tags(crew),
            *cls._get_level_tags(crew),
            *cls._get_custom_tags(crew),
        ]

    @classmethod
    def _get_language_tags(cls, crew: models.Crew) -> Iterable[dto.CrewTag]:
        submittable_languages = models.CrewSubmittableLanguage.objects.filter(**{
            models.CrewSubmittableLanguage.field_name.CREW: crew,
        })
        for submittable_language in submittable_languages.all():
            programming_language = enums.ProgrammingLanguageChoices(
                submittable_language.language)
            yield dto.CrewTag(
                key=programming_language.value,
                name=programming_language.label,
                type=enums.CrewTagType.LANGUAGE,
            )

    @classmethod
    def _get_level_tags(cls, crew: models.Crew) -> Iterable[dto.CrewTag]:
        if crew.min_boj_level is not None:
            min_boj_level = UserBojLevelChoices(crew.min_boj_level)
        else:
            min_boj_level = UserBojLevelChoices.U
        # 보여질 문구를 결정
        if min_boj_level == UserBojLevelChoices.U:
            name = '티어 무관'
        elif min_boj_level.get_tier() == 5:
            name = f"{min_boj_level.get_division_name(lang='ko')} 이상"
        else:
            name = f"{min_boj_level.get_name(lang='ko', arabic=False)} 이상"
        yield dto.CrewTag(
            key=None,
            name=name,
            type=enums.CrewTagType.LEVEL,
        )

    @classmethod
    def _get_custom_tags(cls, crew: models.Crew) -> Iterable[dto.CrewTag]:
        for tag in crew.custom_tags:
            yield dto.CrewTag(
                key=None,
                name=tag,
                type=enums.CrewTagType.CUSTOM,
            )

    @staticmethod
    def member_count(crew: models.Crew) -> int:
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: crew,
        }).count()

    @classmethod
    def is_joinable(cls, crew: models.Crew, user: User) -> bool:
        if not crew.is_recruiting:
            return False
        if cls.member_count(crew) >= crew.max_members:
            return False
        if cls.is_member(crew, user):
            return False
        if crew.min_boj_level is not None:
            return bool(
                (user.boj_level is not None) and
                (user.boj_level >= crew.min_boj_level)
            )
        return True

    @staticmethod
    def is_member(crew: models.Crew, user: User) -> bool:
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: crew,
            models.CrewMember.field_name.USER: user,
        }).exists()


class crew_acitivity:
    @staticmethod
    def of_crew(crew: models.Crew, exclude_future=True) -> QuerySet[models.CrewActivity]:
        """
        exclude_future: 아직 공개되지 않은 활동도 포함할 지 여부.
        """
        kwargs = {
            models.CrewActivity.field_name.CREW: crew,
        }
        if exclude_future:
            kwargs[models.CrewActivity.field_name.START_AT +
                   '__lte'] = timezone.now()
        return models.CrewActivity.objects.filter(**kwargs).order_by(models.CrewActivity.field_name.START_AT)

    @staticmethod
    def is_opened(activity: models.CrewActivity) -> bool:
        """활동이 진행 중인지 여부를 반환합니다."""
        assert isinstance(activity, models.CrewActivity)
        return activity.start_at <= timezone.now() <= activity.end_at

    @staticmethod
    def is_closed(activity: models.CrewActivity) -> bool:
        """활동이 종료되었는지 여부를 반환합니다."""
        assert isinstance(activity, models.CrewActivity)
        return activity.end_at < timezone.now()

    @staticmethod
    def number(activity: models.CrewActivity) -> int:
        assert isinstance(activity, models.CrewActivity)
        """활동의 회차 번호를 반환합니다.

        이 값은 1부터 시작합니다.
        자신의 활동 시작일자보다 이전에 시작된 활동의 개수를 센 값에 1을
        더한 값을 반환하므로, 고정된 값이 아닙니다.
        """
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: activity.crew,
            models.CrewActivity.field_name.START_AT+'__lte': activity.start_at,
        }).count()


class crew_applicant:
    @staticmethod
    def notify_captain(applicant: models.CrewApplicant):
        assert isinstance(applicant, models.CrewApplicant)
        captain = models.CrewMember.objects.get(**{
            models.CrewMember.field_name.CREW: applicant.crew,
            models.CrewMember.field_name.IS_CAPTAIN: True,
        })
        send_mail(
            subject='[Time Limit Exceeded] 새로운 크루 가입 신청',
            message=dedent(f"""
                [{applicant.crew.icon} {applicant.crew.name}]에 새로운 가입 신청이 왔어요!

                지원자의 메시지:
                ```
                {applicant.message}
                ```

                수락하시려면 [여기]를 클릭해주세요.
            """),
            from_email=None,
            recipient_list=[captain.user.email],
            fail_silently=False,
        )

    @staticmethod
    def notify_accepted(applicant: models.CrewApplicant):
        assert isinstance(applicant, models.CrewApplicant)
        assert applicant.is_accepted
        send_mail(
            subject=f"""[Time Limit Exceeded] 크루 가입 신청이 승인되었습니다""",
            message=dedent(f"""
                [{applicant.crew.icon} {applicant.crew.name}]에 가입하신 것을 축하해요!

                [여기]를 눌러 크루 대시보드로 바로가기
            """),
            from_email=None,
            recipient_list=[applicant.user.email],
            fail_silently=False,
        )

    @staticmethod
    def notify_rejected(applicant: models.CrewApplicant):
        assert isinstance(applicant, models.CrewApplicant)
        assert not applicant.is_accepted
        send_mail(
            subject=f"""[Time Limit Exceeded] 크루 가입 신청이 거절되었습니다""",
            message=dedent(f"""
                [{applicant.crew.icon} {applicant.crew.name}]에 아쉽게도 가입하지 못했어요!
            """),
            from_email=None,
            recipient_list=[applicant.user.email],
            fail_silently=False,
        )

    @staticmethod
    def accept(applicant: models.CrewApplicant, reviewed_by: User):
        with atomic():
            applicant.is_accepted = True
            applicant.reviewed_at = timezone.now()
            applicant.reviewed_by = reviewed_by
            applicant.save()
            models.CrewMember.objects.create(**{
                models.CrewApplicant.field_name.CREW: applicant.crew,
                models.CrewApplicant.field_name.USER: applicant.user,
            })

    @staticmethod
    def reject(applicant: models.CrewApplicant, reviewed_by: User):
        applicant.is_accepted = False
        applicant.reviewed_at = timezone.now()
        applicant.reviewed_by = reviewed_by
        applicant.save()
