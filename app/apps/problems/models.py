from django.db import models

from apps.problems.dto import ProblemDTO
from apps.problems.enums import Unit
from users.models import User


class Problem(models.Model):
    title = models.CharField(
        max_length=100,
        help_text='문제 이름을 입력해주세요.',
    )
    link = models.URLField(
        help_text='문제 링크를 입력해주세요. (선택)',
        blank=True,
    )
    description = models.TextField(
        help_text='문제 설명을 입력해주세요.',
    )
    input_description = models.TextField(
        help_text='문제 입력 설명을 입력해주세요.',
    )
    output_description = models.TextField(
        help_text='문제 출력 설명을 입력해주세요.',
    )
    memory_limit = models.FloatField(
        help_text='문제 메모리 제한을 입력해주세요. (MB 단위)',
    )
    memory_limit_unit = models.TextField(
        choices=Unit.choices,
        default=Unit.MEGA_BYTE,
    )
    time_limit = models.FloatField(
        help_text='문제 시간 제한을 입력해주세요. (초 단위)',
    )
    time_limit_unit = models.TextField(
        choices=Unit.choices,
        default=Unit.SECOND,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        help_text='이 문제를 추가한 사용자를 입력해주세요.',
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class field_name:
        TITLE = 'title'
        LINK = 'link'
        DESCRIPTION = 'description'
        INPUT_DESCRIPTION = 'input_description'
        OUTPUT_DESCRIPTION = 'output_description'
        MEMORY_LIMIT = 'memory_limit'
        MEMORY_LIMIT_UNIT = 'memory_limit_unit'
        TIME_LIMIT = 'time_limit'
        TIME_LIMIT_UNIT = 'time_limit_unit'
        CREATED_AT = 'created_at'
        CREATED_BY = 'created_by'
        UPDATED_AT = 'updated_at'

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'[{self.pk} : {self.title}]'

    def as_dto(self) -> ProblemDTO:
        return ProblemDTO(
            id=self.pk,
            title=self.title,
            description=self.description,
            input_description=self.input_description,
            output_description=self.output_description,
            memory_limit=self.memory_limit,
            time_limit=self.time_limit,
        )
