from django.core.validators import MinValueValidator
from django.db import models

from crews.models.crew import Crew
from crews.models.crew_activity import CrewActivity
from problems.models.problem import Problem


class CrewActivityProblem(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    activity = models.ForeignKey(
        CrewActivity,
        on_delete=models.CASCADE,
        help_text='활동을 입력해주세요.',
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.PROTECT,
        help_text='문제를 입력해주세요.',
    )
    order = models.IntegerField(
        help_text='문제 순서를 입력해주세요.',
        validators=[
            MinValueValidator(1),
        ],
    )

    class field_name:
        # related fields
        SUBMISSIONS = 'submissions'
        # fields
        CREW = 'crew'
        ACTIVITY = 'activity'
        PROBLEM = 'problem'
        ORDER = 'order'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['activity', 'order'],
                name='unique_order_per_activity_problem',
            ),
        ]
        ordering = ['order']

    def save(self, *args, **kwargs) -> None:
        assert self.crew == self.activity.crew
        return super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return f'{self.activity.__repr__()} ← #{self.order} {self.problem.__repr__()}'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()}'
