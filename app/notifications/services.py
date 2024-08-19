import logging
from textwrap import dedent

from django.core.mail import send_mail

import crews.models
import users.models


SUBJECT_PREFIX = '[Time Limit Exceeded]'

LOGGER = logging.getLogger('mail_admins')


def notify_crew_application_requested(applicant: crews.models.CrewApplicant):
    assert isinstance(applicant, crews.models.CrewApplicant)
    send_mail(
        subject=f'{SUBJECT_PREFIX} 새로운 크루 가입 신청',
        message=dedent(f"""
            [{applicant.crew.icon} {applicant.crew.name}]에 새로운 가입 신청이 왔어요!

            지원자: {applicant.user.username}
            지원자의 백준 아이디(레벨): {applicant.user.boj_username} ({users.models.UserBojLevelChoices(applicant.user.boj_level).get_name(lang='ko', arabic=False)})

            지원자의 메시지:
            ```
            {applicant.message}
            ```

            수락하시려면 [여기]를 클릭해주세요.
        """),
        recipient_list=[applicant.crew.created_by.email],
        from_email=None,
        fail_silently=False,
    )
    LOGGER.info(f'MAIL crew.application.requested {applicant.crew.created_by.email}')


def notify_crew_application_accepted(applicant: crews.models.CrewApplicant):
    assert isinstance(applicant, crews.models.CrewApplicant)
    send_mail(
        subject=f'{SUBJECT_PREFIX} 새로운 크루 가입 신청이 승인되었습니다',
        message=dedent(f"""
            [{applicant.crew.icon} {applicant.crew.name}]에 가입하신 것을 축하해요!

            [여기]를 눌러 크루 대시보드로 바로가기
        """),
        recipient_list=[applicant.user.email],
        from_email=None,
        fail_silently=False,
    )
    LOGGER.info(f'MAIL crew.application.accepted {applicant.user.email}')


def notify_crew_application_rejected(applicant: crews.models.CrewApplicant):
    assert isinstance(applicant, crews.models.CrewApplicant)
    send_mail(
        subject=f'{SUBJECT_PREFIX} 새로운 크루 가입 신청이 거절되었습니다',
        message=dedent(f"""
            [{applicant.crew.icon} {applicant.crew.name}]에 아쉽게도 가입하지 못했어요!
        """),
        recipient_list=[applicant.user.email],
        from_email=None,
        fail_silently=False,
    )
    LOGGER.info(f'MAIL crew.application.rejected {applicant.user.email}')
