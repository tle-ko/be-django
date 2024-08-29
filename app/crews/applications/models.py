from __future__ import annotations

from typing import Union

from django.db import models

from crews.models import Crew
from users.models import User


class CrewApplicationManager(models.Manager):
    def crew(self, crew: Crew) -> _CrewApplicationManager:
        return self.filter(**{CrewApplication.field_name.CREW: crew})

    def applicant(self, user: User) -> _CrewApplicationManager:
        return self.filter(**{CrewApplication.field_name.APPLICANT: user})


class CrewApplication(models.Model):
    crew = models.ForeignKey[Crew](
        Crew,
        on_delete=models.CASCADE,
        help_text='크루를 입력해주세요.',
    )
    applicant = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        help_text='지원자를 입력해주세요.',
    )
    message = models.TextField(
        help_text='가입 메시지를 입력해주세요.',
        null=True,
        blank=True,
    )
    is_pending = models.BooleanField(
        default=True,
        help_text="아직 수락/거절 되지 않았다면 True.",
    )
    is_accepted = models.BooleanField(
        default=False,
        help_text='수락 여부를 입력해주세요.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(
        help_text='리뷰한 시간을 입력해주세요.',
        null=True,
        blank=True,
        default=None,
    )
    reviewed_by = models.ForeignKey[User](
        User,
        related_name='reviewed_applicants',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    objects: _CrewApplicationManager = CrewApplicationManager()

    class field_name:
        CREW = 'crew'
        APPLICANT = 'applicant'
        MESSAGE = 'message'
        IS_PENDING = 'is_pending'
        IS_ACCEPTED = 'is_accepted'
        CREATED_AT = 'created_at'
        REVIEWED_AT = 'reviewed_at'
        REVIEWED_BY = 'reviewed_by'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'applicant'],
                condition=models.Q(is_pending=True),
                name='unique_pending_application',
            ),
        ]
        ordering = ['reviewed_by', 'created_at']

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.applicant.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'


_CrewApplicationManager = Union[CrewApplicationManager,
                                models.Manager[CrewApplication]]
