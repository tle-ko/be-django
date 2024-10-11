from django.contrib import admin
from django.db.models import QuerySet

from . import models


@admin.register(models.TextGenerationDAO)
class TextGenerationModelAdmin(admin.ModelAdmin):
    list_display = [
        models.TextGenerationDAO.field_name.PK,
        models.TextGenerationDAO.field_name.REQUEST,
        models.TextGenerationDAO.field_name.RESPONSE,
        models.TextGenerationDAO.field_name.CREATED_AT,
    ]
    ordering = [
        '-'+models.TextGenerationDAO.field_name.CREATED_AT,
    ]
    actions = [
        'action_generate',
    ]

    @admin.action(description="선택된 객체에 대해 LLM에 질의를 시도합니다.")
    def action_generate(self, request, queryset: QuerySet[models.TextGenerationDAO]):
        for obj in queryset:
            obj.generate()
