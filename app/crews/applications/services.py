from textwrap import dedent

from background_task import background
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from boj.enums import BOJLevel
from boj.models import BOJUser
from crews.applications.models import CrewApplication
from crews.applications.signals import reviewed
from crews.models import Crew
from crews.models import CrewMember
from users.models import User


def apply(crew: Crew, applicant: User, message: str) -> CrewApplication:
    is_valid_applicant(crew, applicant, raise_exception=True)
    return CrewApplication.objects.create(**{
        CrewApplication.field_name.CREW: crew,
        CrewApplication.field_name.APPLICANT: applicant,
        CrewApplication.field_name.MESSAGE: message,
    })


def is_valid_applicant(crew: Crew, applicant: User, raise_exception=False) -> bool:
    try:
        boj_user = BOJUser.objects.get_by_user(applicant)
        assert crew.is_recruiting, (
            "'크루가 현재 크루원을 모집하고 있지 않습니다."
        )
        assert CrewMember.objects.filter(crew=crew).count() < crew.max_members, (
            "크루의 최대 정원을 초과하였습니다."
        )
        assert not CrewMember.objects.filter(crew=crew, user=applicant).exists(), (
            "이미 가입한 크루입니다."
        )
        assert (crew.min_boj_level is None) or (crew.min_boj_level <= boj_user.level), (
            "최소 백준 티어 요구조건을 달성하지 못하였습니다."
        )
    except AssertionError as exception:
        if raise_exception:
            raise ValidationError from exception
        return False
    else:
        return True


def accept(instance: CrewApplication, reviewed_by: User):
    review(instance, reviewed_by, accept=True)


def reject(instance: CrewApplication, reviewed_by: User):
    review(instance, reviewed_by, accept=False)


def review(instance: CrewApplication, reviewed_by: User, accept: bool):
    instance.is_pending = False
    instance.is_accepted = accept
    instance.reviewed_by = reviewed_by
    instance.reviewed_at = timezone.now()
    instance.save()
    reviewed.send(sender=CrewApplication, instance=instance)


@receiver(post_save, sender=CrewApplication)
def notify_on_applied(sender, instance: CrewApplication, created: bool, **kwargs):
    if created:
        notify_application_recieved(instance)


@receiver(reviewed, sender=CrewApplication)
def notify_on_reviewed(sender, instance: CrewApplication, **kwargs):
    assert not instance.is_pending
    if instance.is_accepted:
        notify_application_accepted(instance)
    else:
        notify_application_rejected(instance)


def notify_application_recieved(instance: CrewApplication):
    captain = CrewMember.objects.filter(crew=instance.crew, is_captain=True).get()
    boj_user = BOJUser.objects.get(username=instance.applicant.boj_username)
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 도착했습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 새로운 가입 신청이 왔어요!

        지원자: {instance.applicant.username}
        지원자의 백준 아이디(레벨): {boj_user.username} ({BOJLevel(boj_user.level).get_name(lang='ko', arabic=False)})

        지원자의 메시지:
        ```
        {instance.message}
        ```

        수락하시려면 [여기]를 클릭해주세요.
    """)
    recipient = captain.user.email
    _schedule_mail(subject, message, recipient)


def notify_application_accepted(instance: CrewApplication):
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 승인되었습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 가입하신 것을 축하해요!

        [여기]를 눌러 크루 대시보드로 바로가기
    """)
    recipient = instance.applicant.email
    _schedule_mail(subject, message, recipient)


def notify_application_rejected(instance: CrewApplication):
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 거절되었습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 아쉽게도 가입하지 못했어요.
    """)
    recipient = instance.applicant.email
    _schedule_mail(subject, message, recipient)


@background
def _schedule_mail(subject: str, message: str, recipient: str) -> None:
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient],
        from_email=None,
        fail_silently=False,
    )
