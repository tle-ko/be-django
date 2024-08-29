from textwrap import dedent
from typing import List

from background_task import background
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from boj.enums import BOJLevel
from app.crews.servicesa import dto
from crews import enums
from crews import models
from crews.servicesa.base import UserCrewService
from crews.servicesa.base import CrewService
from crews.servicesa.base import CrewActivityService
from crews.servicesa.base import CrewApplicantionService
from problems.dto import ProblemStatisticDTO
from problems.models import Problem
from users.models import User


class ConcreteUserCrewService(UserCrewService):
    def query_crews_joined(self) -> QuerySet[models.Crew]:
        # 활동 종료된 크루는 뒤로 가도록 정렬
        return models.Crew.objects.filter(
            pk__in=self._crew_ids_list_joined(),
        ).order_by(
            '-'+models.Crew.field_name.IS_ACTIVE,
        )

    def query_crews_recruiting(self) -> QuerySet[models.Crew]:
        return models.Crew.objects.filter(**{
            models.Crew.field_name.IS_RECRUITING: True,
        }).exclude(
            pk__in=self._crew_ids_list_joined(),
        )

    def _crew_ids_list_joined(self) -> List[int]:
        if not self.instance.is_authenticated:
            return []
        return models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.USER: self.instance,
        }).values_list(models.CrewMember.field_name.CREW)


class ConcreteCrewService(CrewService):
    def query_members(self) -> QuerySet[models.CrewMember]:
        ...

    def query_languages(self) -> QuerySet[models.CrewSubmittableLanguage]:
        ...

    def query_applications(self) -> QuerySet[models.CrewApplication]:
        ...

    def query_activities(self) -> QuerySet[models.CrewActivity]:
        ...

    def query_activities_published(self) -> QuerySet[models.CrewActivity]:
        ...

    def query_problems(self) -> QuerySet[Problem]:
        ...

    def query_captain(self) -> QuerySet[models.CrewMember]:
        ...

    def statistics(self) -> ProblemStatisticDTO:
        ...

    def display_name(self) -> str:
        ...

    def tags(self) -> List[dto.CrewTag]:
        ...

    def languages(self) -> List[enums.ProgrammingLanguageChoices]:
        ...

    def min_boj_level(self) -> BOJLevel:
        ...

    def is_captain(self, user: User) -> bool:
        ...

    def is_member(self, user: User) -> bool:
        ...

    def set_languages(self, languages: List[enums.ProgrammingLanguageChoices]) -> None:
        ...

    def apply(self, applicant: User, message: str) -> models.CrewApplication:
        ...

        # send notification
        subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 도착했습니다'
        message=dedent(f"""
            [{self.instance.crew.icon} {self.instance.crew.name}]에 새로운 가입 신청이 왔어요!

            지원자: {applicant.applicant.username}
            지원자의 백준 아이디(레벨): {applicant.applicant.boj_username} ({users.models.UserBojLevelChoices(applicant.applicant.boj_level).get_name(lang='ko', arabic=False)})

            지원자의 메시지:
            ```
            {applicant.message}
            ```

            수락하시려면 [여기]를 클릭해주세요.
        """)
        recipient=self.query_captain().get().user.email
        schedule_mail(subject, message, recipient)

    def validate_applicant(self, applicant: User, raises_exception=False) -> bool:
        ...


class ConcreteCrewActivityService(CrewActivityService):
    def query_previous_activities(self) -> QuerySet[models.CrewActivity]:
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: self.instance.crew,
            models.CrewActivity.field_name.START_AT+'__lt': self.instance.start_at,
        })

    def nth(self) -> int:
        return self.query_previous_activities().count()+1

    def is_in_progress(self) -> bool:
        return self.has_started() and not self.has_ended()

    def has_started(self) -> bool:
        return self.instance.start_at <= timezone.now()

    def has_ended(self) -> bool:
        return self.instance.end_at < timezone.now()


class ConcreteCrewApplicantionService(CrewApplicantionService):
    def reject(self, reviewed_by: User):
        self.instance.is_pending = False
        self.instance.is_accepted = True
        self.instance.reviewed_by = reviewed_by
        self.instance.reviewed_at = timezone.now()
        self.instance.save()

        # send notification
        subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 거절되었습니다'
        message=dedent(f"""
            [{self.instance.crew.icon} {self.instance.crew.name}]에 아쉽게도 가입하지 못했어요.
        """)
        recipient=self.instance.applicant.email
        schedule_mail(subject, message, recipient)

    def accept(self, reviewed_by: User):
        self.instance.is_pending = False
        self.instance.is_accepted = False
        self.instance.reviewed_by = reviewed_by
        self.instance.reviewed_at = timezone.now()
        with atomic():
            self.instance.save()
            self._save_member()

        # send notification
        subject='[Time Limit Exceeded] 새로운 크루 가입 신청이 승인되었습니다'
        message=dedent(f"""
            [{self.instance.crew.icon} {self.instance.crew.name}]에 가입하신 것을 축하해요!

            [여기]를 눌러 크루 대시보드로 바로가기
        """)
        recipient=self.instance.applicant.email
        schedule_mail(subject, message, recipient)

    def _save_member(self) -> models.CrewMember:
        return models.CrewMember.objects.create(**{
            models.CrewApplication.field_name.CREW: self.instance.crew,
            models.CrewApplication.field_name.APPLICANT: self.instance.applicant,
        })


@background
def schedule_mail(subject: str, message: str, recipient: str) -> None:
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient],
        from_email=None,
        fail_silently=False,
    )
