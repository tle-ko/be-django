import typing

from django.db import models

from tle.models.user import User


class Problem(models.Model):
    title = models.CharField(
        max_length=100,
        help_text='문제 이름을 입력해주세요.',
        blank=False,
    )
    link = models.URLField(
        help_text='문제 링크를 입력해주세요. (선택)',
        blank=True,
    )
    description = models.TextField(
        help_text='문제 설명을 입력해주세요.',
        blank=False,
    )
    input_description = models.TextField(
        help_text='문제 입력 설명을 입력해주세요.',
        blank=True,
    )
    output_description = models.TextField(
        help_text='문제 출력 설명을 입력해주세요.',
        blank=True,
    )
    memory_limit_megabyte = models.FloatField(
        help_text='문제 메모리 제한을 입력해주세요. (MB 단위)',
    )
    time_limit_second = models.FloatField(
        help_text='문제 시간 제한을 입력해주세요. (초 단위)',
        default=1.0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name=User.field_name.PROBLEMS,
        help_text='이 문제를 추가한 사용자를 입력해주세요.',
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    if typing.TYPE_CHECKING:
        import tle.models as t

        analysis: models.OneToOneField[t.ProblemAnalysis]
        activity_problems: models.ManyToOneRel[t.CrewActivityProblem]

    class field_name:
        # related fields
        ANALYSIS = 'analysis'
        ACTIVITY_PROBLEMS = 'activity_problems'
        # fields
        TITLE = 'title'
        LINK = 'link'
        DESCRIPTION = 'description'
        INPUT_DESCRIPTION = 'input_description'
        OUTPUT_DESCRIPTION = 'output_description'
        MEMORY_LIMIT_MEGABYTE = 'memory_limit_megabyte'
        TIME_LIMIT_SECOND = 'time_limit_second'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['-created_at']

    MEMORY_LIMIT_UNIT = {
        "name_ko": "메가 바이트",
        "name_en": "Mega Bytes",
        "abbr": "MB",
    }

    TIME_LIMIT_UNIT = {
        "name_ko": "초",
        "name_en": "Seconds",
        "abbr": "s",
    }

    def __repr__(self) -> str:
        return f'[{self.title}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ← {self.created_by.__repr__()}'
