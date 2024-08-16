from __future__ import annotations

from django.contrib import admin
from django.db import models
from django.utils import timezone

from crews.models.crew import Crew


class CrewActivity(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
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

    class field_name:
        CREW = 'crew'
        NAME = 'name'
        START_AT = 'start_at'
        END_AT = 'end_at'

    class Meta:
        ordering = ['start_at']
        get_latest_by = ['end_at']

    def __str__(self) -> str:
        return f"[{self.pk}: {self.name} ({self.start_at.date()} ~ {self.end_at.date()})]"
