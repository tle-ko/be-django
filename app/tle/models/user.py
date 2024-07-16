import typing

from django.contrib.auth.models import User as BaseUser
from django.db import models


class User(BaseUser):
    image = models.ImageField(
        help_text='프로필 이미지',
        upload_to='user_images/',
        null=True,
        blank=True,
        validators=[
            # TODO: 이미지 크기 제한
            # TODO: 이미지 확장자 제한
        ]
    )
    boj_id = models.CharField(
        help_text='백준 아이디',
        max_length=40,
        null=True,
        blank=True,
    )

    @property
    def crews(self):
        for member in self.members:
            yield member.crew

    REQUIRED_FIELDS = [
        'email',
        'username',
        'password',
    ]

    class FieldName:
        PROBLEMS = 'problems'
        APPLICANTS = 'applicants'
        MEMBERS = 'members'
        SUBMISSIONS = 'submissions'

    if typing.TYPE_CHECKING:
        from . import (
            Problem as T_Problem,
            Crew as T_Crew,
            CrewApplicant as T_CrewApplicant,
            CrewMember as T_CrewMember,
            Submission as T_Submission,
        )
        problems: models.QuerySet[T_Problem]
        applicants: models.QuerySet[T_CrewApplicant]
        members: models.QuerySet[T_CrewMember]
        submissions: models.QuerySet[T_Submission]

    def __repr__(self) -> str:
        return f'[@{self.username}]'

    def __str__(self) -> str:
        staff = '(관리자)' if self.is_staff else ''
        return f'{self.pk} : {self.__repr__()} {staff}'


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
