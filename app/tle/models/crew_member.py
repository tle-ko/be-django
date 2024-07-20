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
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        CREW = 'crew'
        USER = 'user'
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
        return cls.objects.get(crew=crew, user=crew.created_by)

    def __repr__(self) -> str:
        return f'[{self.crew.icon} {self.crew.name}] ← [@{self.user.username}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'

    def is_captain(self) -> bool:
        return self.crew.created_by == self.user
