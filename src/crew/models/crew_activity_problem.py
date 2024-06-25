from django.core.validators import MinValueValidator
from django.db import models

from crew.models.crew_activity import CrewActivity
from problem.models import Problem


class CrewActivityProblem(models.Model):
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.CASCADE,
        related_name='problems',
        help_text=(
            '활동을 입력해주세요.'
        ),
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        related_name='activities',
        help_text=(
            '문제를 입력해주세요.'
        ),
    )
    order = models.IntegerField(
        help_text=(
            '문제 순서를 입력해주세요.'
        ),
        validators=[
            MinValueValidator(1),
            # TODO: 다른 문제 순서와 겹치지 않도록 검사
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
