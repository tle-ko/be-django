from django.db import models

from crew.models.crew import Crew
from user.models import User


class CrewMemberRequest(models.Model):
    # TODO: 같은 크루에 여러 번 가입하는 것을 막기 위한 로직 추가
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='requests',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='crew_requests',
        help_text=(
            '유저를 입력해주세요.'
        ),
    )
    message = models.TextField(
        help_text=(
            '가입 메시지를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← {self.user.__repr__()} : "{self.message}"'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
