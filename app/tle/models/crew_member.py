from __future__ import annotations

from django.db import models, transaction

from tle.models.user import User
from tle.models.crew import Crew


class CrewMember(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name=Crew.field_name.MEMBERS,
        help_text='크루를 입력해주세요.',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name=User.field_name.MEMBERS,
        help_text='유저를 입력해주세요.',
    )
    is_captain = models.BooleanField(
        default=False,
        help_text='선장인지 여부를 입력해주세요.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        CREW = 'crew'
        USER = 'user'
        IS_CAPTAIN = 'is_captain'
        CREATED_AT = 'created_at'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crew', 'is_captain'],
                name='unique_captain_per_crew'
            ),
            models.UniqueConstraint(
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['is_captain', 'created_at']

    def __repr__(self) -> str:
        return f'[{self.crew.icon} {self.crew.name}] ← [@{self.user.username}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'

    def make_captain(self, commit=True) -> CrewMember:
        """전 선장을 직위해제하고, 이 멤버를 새로운 선장으로 임명합니다.

        전 선장에 대한 엔티티를 반환합니다.

        TODO: 크루장이 탈퇴할 경우 새로운 크루장은 어떻게 선발할 지 검토
        TODO: 크루장이 여러 명일 경우 어떻게 처리할 지 검토 (예외 처리)
        """
        def inner():
            former_captain = self.crew.members.get(is_captain=True)
            former_captain.is_captain = False
            self.is_captain = True
            return former_captain

        if not commit:
            return inner()

        with transaction.atomic():
            former_captain = inner()
            former_captain.save()
            self.save()
            return former_captain
