from django.db import models

from tle.models.crew import Crew


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text='크루를 입력해주세요.',
    )
    name = models.TextField(
        help_text='활동 이름을 입력해주세요. (예: "1회차")',
    )
    start_at = models.DateTimeField(
        help_text='활동 시작 일자를 입력해주세요.',
    )
    end_at = models.DateTimeField(
        help_text='활동 종료 일자를 입력해주세요.',
    )

    def __repr__(self) -> str:
        return f'{self.crew.__repr__()} ← [{self.start_at.date()} ~ {self.end_at.date()}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
