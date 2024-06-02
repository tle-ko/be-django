from django.core.validators import MinValueValidator
from django.db import models

from problem.models import Problem
from crew.models.crew import Crew


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text=(
            '크루를 입력해주세요.'
        ),
    )
    start_at = models.DateTimeField(
        help_text=(
            '활동 시작 일자를 입력해주세요.'
        ),
    )
    end_at = models.DateTimeField(
        help_text=(
            '활동 종료 일자를 입력해주세요.'
        ),
    )


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
