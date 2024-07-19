import typing

from django.core.validators import MinValueValidator
from django.db import models

from tle.models.crew_activity import CrewActivity
from tle.models.problem import Problem


class CrewActivityProblem(models.Model):
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.CASCADE,
        related_name=CrewActivity.field_name.PROBLEMS,
        help_text='활동을 입력해주세요.',
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        related_name=Problem.field_name.ACTIVITY_PROBLEMS,
        help_text='문제를 입력해주세요.',
    )
    order = models.IntegerField(
        help_text='문제 순서를 입력해주세요.',
        validators=[
            MinValueValidator(1),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    if typing.TYPE_CHECKING:
        import tle.models as t

        submissions: models.ManyToOneRel[t.Submission]

    class field_name:
        # related fields
        SUBMISSIONS = 'submissions'
        # fields
        ACTIVITY = 'activity'
        PROBLEM = 'problem'
        ORDER = 'order'
        CREATED_AT = 'created_at'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'order'],
                name='unique_order_per_activity_problem',
            ),
        ]
        ordering = ['order']

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
