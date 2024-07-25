from __future__ import annotations

from django.db import models

from tle.models.dao.user import User
from tle.models.dao.crew import Crew


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
        help_text='크루장 여부',
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
                fields=['crew', 'user'],
                name='unique_member_per_crew'
            ),
        ]
        ordering = ['created_at']

    @classmethod
    def captain_of(cls, crew: Crew) -> CrewMember:
        return cls.objects.get(**{
            CrewMember.field_name.CREW: crew,
            CrewMember.field_name.IS_CAPTAIN: True,
        })
