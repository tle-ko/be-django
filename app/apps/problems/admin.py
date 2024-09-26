from django.contrib import admin
from django.db.models import QuerySet

from apps.boj.proxy import BOJTag
from users.models import User

from . import analyzer
from . import models


@admin.register(models.ProblemDAO)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemDAO.field_name.TITLE,
        models.ProblemDAO.field_name.CREATED_BY,
        models.ProblemDAO.field_name.CREATED_AT,
        models.ProblemDAO.field_name.UPDATED_AT,
    ]
    search_fields = [
        models.ProblemDAO.field_name.TITLE,
        models.ProblemDAO.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
    ]
    ordering = ['-'+models.ProblemDAO.field_name.CREATED_AT]
    actions = [
        'action_schedule_analyze',
        'action_copy',
    ]

    @admin.action(description="Schedule to analyze selected problems.")
    def action_schedule_analyze(self, request, queryset: QuerySet[models.ProblemDAO]):
        for obj in queryset:
            analyzer.schedule_analysis(obj.pk)

    @admin.action(description="Create copies of selected problems.")
    def action_copy(self, request, queryset: QuerySet[models.ProblemDAO]):
        for obj in queryset:
            models.ProblemDAO.objects.create(
                title=obj.title,
                link=obj.link,
                description=obj.description,
                input_description=obj.input_description,
                output_description=obj.output_description,
                memory_limit=obj.memory_limit,
                memory_limit_unit=obj.memory_limit_unit,
                time_limit=obj.time_limit,
                time_limit_unit=obj.time_limit_unit,
                created_by=obj.created_by,
            )


@admin.register(models.ProblemAnalysisDAO)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysisDAO.field_name.PROBLEM,
        models.ProblemAnalysisDAO.field_name.DIFFICULTY,
        'get_time_complexity',
        'get_tags',
        'get_hint_steps',
        models.ProblemAnalysisDAO.field_name.CREATED_AT,
    ]
    search_fields = [
        models.ProblemAnalysisDAO.field_name.PROBLEM+'__'+models.ProblemDAO.field_name.TITLE,
        models.ProblemAnalysisDAO.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+models.ProblemAnalysisDAO.field_name.CREATED_AT]

    @admin.display(description='Time complexity')
    def get_time_complexity(self, obj: models.ProblemAnalysisDAO) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, analysis: models.ProblemAnalysisDAO) -> str:
        tag_keys = models.ProblemAnalysisTagDAO.objects.filter(**{
            models.ProblemAnalysisTagDAO.field_name.ANALYSIS: analysis,
        }).select_related(
            models.ProblemAnalysisTagDAO.field_name.TAG,
        ).values_list(
            models.ProblemAnalysisTagDAO.field_name.TAG+'__'+BOJTag.field_name.KEY,
            flat=True,
        )
        return ', '.join(tag_keys)

    @admin.display(description='Hint steps')
    def get_hint_steps(self, obj: models.ProblemAnalysisDAO) -> int:
        return len(obj.hints)


@admin.register(models.ProblemAnalysisTagDAO)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysisTagDAO.field_name.ANALYSIS,
        models.ProblemAnalysisTagDAO.field_name.TAG,
    ]
    ordering = [models.ProblemAnalysisTagDAO.field_name.ANALYSIS]
