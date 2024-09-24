from django.contrib import admin
from django.db.models import QuerySet

from . import proxy


@admin.register(proxy.TextGeneration)
class TextGenerationModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.TextGeneration.field_name.PK,
        proxy.TextGeneration.field_name.REQUEST,
        proxy.TextGeneration.field_name.RESPONSE,
        proxy.TextGeneration.field_name.CREATED_AT,
    ]
    ordering = [
        '-'+proxy.TextGeneration.field_name.CREATED_AT,
    ]
    actions = [
        'action_generate',
    ]

    @admin.action(description="선택된 객체에 대해 LLM에 질의를 시도합니다.")
    def action_generate(self, request, queryset: QuerySet[proxy.TextGeneration]):
        for obj in queryset:
            obj.generate()
