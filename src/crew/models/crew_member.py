from django.db import models

from crew.models.crew import Crew
from user.models import User


class CrewMember(models.Model):
    # TODO: 같은 크루에 여러 번 가입하는 것을 막기 위한 로직 추가
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='members',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='crews',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'[{self.crew.emoji} {self.crew.name}] ← [@{self.user.username}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
