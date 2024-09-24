from django.contrib import admin
from django.db.models import QuerySet

from apps.analyses.analyzers import schedule_analyze
from apps.analyses.analyzers import analyze
from apps.problems.proxy import Problem
from users.models import User


@admin.register(Problem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        Problem.field_name.TITLE,
        Problem.field_name.CREATED_BY,
        Problem.field_name.CREATED_AT,
        Problem.field_name.UPDATED_AT,
    ]
    search_fields = [
        Problem.field_name.TITLE,
        Problem.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
    ]
    ordering = ['-'+Problem.field_name.CREATED_AT]
    actions = [
        'action_analyze',
        'action_schedule_analyze',
    ]

    @admin.action(description="Analyze selected problems.")
    def action_analyze(self, request, queryset: QuerySet[Problem]):
        for obj in queryset:
            analyze(obj.pk)

    @admin.action(description="Schedule to analyze selected problems.")
    def action_schedule_analyze(self, request, queryset: QuerySet[Problem]):
        for obj in queryset:
            schedule_analyze(obj.pk)
