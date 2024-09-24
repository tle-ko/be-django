from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from apps.boj.enums import BOJLevel
from apps.boj.proxy import BOJUser
from apps.crews.models import CrewMemberDAO
from common.mail import schedule_mail
from users.models import User

if TYPE_CHECKING:
    from . import proxy


def _get_captain(instance: proxy.CrewApplication) -> CrewMemberDAO:
    return CrewMemberDAO.objects.filter(**{
        CrewMemberDAO.field_name.CREW: instance.crew,
        CrewMemberDAO.field_name.IS_CAPTAIN: True,
    }).get()


def _get_bojuser(user: User) -> BOJUser:
    return BOJUser.objects.get(user.boj_username)


def notify_application_recieved(instance: proxy.CrewApplication):
    captain = _get_captain(instance)
    applicant_boj = _get_bojuser(instance.applicant)
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 도착했습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 새로운 가입 신청이 왔어요!

        지원자: {instance.applicant.username}
        지원자의 백준 아이디(레벨): {applicant_boj.username} ({BOJLevel(applicant_boj.level).get_name()})

        지원자의 메시지:
        ```
        {instance.message}
        ```

        수락하시려면 [여기]를 클릭해주세요.
    """)
    recipient = captain.user.email
    schedule_mail(subject, message, recipient)


def notify_application_accepted(instance: proxy.CrewApplication):
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 승인되었습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 가입하신 것을 축하해요!

        [여기]를 눌러 크루 대시보드로 바로가기
    """)
    recipient = instance.applicant.email
    schedule_mail(subject, message, recipient)


def notify_application_rejected(instance: proxy.CrewApplication):
    subject = '[Time Limit Exceeded] 새로운 크루 가입 신청이 거절되었습니다'
    message = dedent(f"""
        [{instance.crew.icon} {instance.crew.name}]에 아쉽게도 가입하지 못했어요.
    """)
    recipient = instance.applicant.email
    schedule_mail(subject, message, recipient)
