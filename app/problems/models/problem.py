from django.db import models

from problems import enums
from users.models import User


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
    memory_limit = models.FloatField(
        help_text='문제 메모리 제한을 입력해주세요. (MB 단위)',
    )
    memory_limit_unit = models.TextField(
        choices=enums.Unit.choices,
        default=enums.Unit.MEGA_BYTE,
    )
    time_limit = models.FloatField(
        help_text='문제 시간 제한을 입력해주세요. (초 단위)',
        default=1.0,
    )
    time_limit_unit = models.TextField(
        choices=enums.Unit.choices,
        default=enums.Unit.SECOND,
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
