from django.contrib import admin
from django.db.models import QuerySet

from apps.boj.proxy import BOJTag
from apps.llms import analyze
from apps.llms import schedule_analyze
from users.models import User

from . import proxy


@admin.register(proxy.Problem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.Problem.field_name.TITLE,
        proxy.Problem.field_name.CREATED_BY,
        proxy.Problem.field_name.CREATED_AT,
        proxy.Problem.field_name.UPDATED_AT,
    ]
    search_fields = [
        proxy.Problem.field_name.TITLE,
        proxy.Problem.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
    ]
    ordering = ['-'+proxy.Problem.field_name.CREATED_AT]
    actions = [
        'action_schedule_analyze',
    ]

    @admin.action(description="Schedule to analyze selected problems.")
    def action_schedule_analyze(self, request, queryset: QuerySet[proxy.Problem]):
        for obj in queryset:
            obj.analyze()


@admin.register(proxy.ProblemAnalysis)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.ProblemAnalysis.field_name.PROBLEM,
        proxy.ProblemAnalysis.field_name.DIFFICULTY,
        'get_time_complexity',
        'get_tags',
        'get_hint_steps',
        proxy.ProblemAnalysis.field_name.CREATED_AT,
    ]
    search_fields = [
        proxy.ProblemAnalysis.field_name.PROBLEM+'__'+proxy.Problem.field_name.TITLE,
        proxy.ProblemAnalysis.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+proxy.ProblemAnalysis.field_name.CREATED_AT]

    @admin.display(description='Time complexity')
    def get_time_complexity(self, obj: proxy.ProblemAnalysis) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, analysis: proxy.ProblemAnalysis) -> str:
        tag_keys = proxy.ProblemAnalysisTag.objects.filter(**{
            proxy.ProblemAnalysisTag.field_name.ANALYSIS: analysis,
        }).select_related(
            proxy.ProblemAnalysisTag.field_name.TAG,
        ).values_list(
            proxy.ProblemAnalysisTag.field_name.TAG+'__'+BOJTag.field_name.KEY,
            flat=True,
        )
        return ', '.join(tag_keys)

    @admin.display(description='Hint steps')
    def get_hint_steps(self, obj: proxy.ProblemAnalysis) -> int:
        return len(obj.hints)


@admin.register(proxy.ProblemAnalysisTag)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.ProblemAnalysisTag.field_name.ANALYSIS,
        proxy.ProblemAnalysisTag.field_name.TAG,
    ]
    ordering = [proxy.ProblemAnalysisTag.field_name.ANALYSIS]
