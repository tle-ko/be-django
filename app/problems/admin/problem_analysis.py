from textwrap import shorten

from django.contrib import admin

from problems import models


@admin.register(models.ProblemAnalysis)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysis.field_name.PROBLEM,
        models.ProblemAnalysis.field_name.DIFFICULTY,
        'get_time_complexity',
        'get_tags',
        'get_hint_steps',
        models.ProblemAnalysis.field_name.CREATED_AT,
    ]
    search_fields = [
        models.ProblemAnalysis.field_name.PROBLEM+'__'+models.Problem.field_name.TITLE,
        models.ProblemAnalysis.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+models.ProblemAnalysis.field_name.CREATED_AT]

    @admin.display(description='Time complexity')
    def get_time_complexity(self, obj: models.ProblemAnalysis) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, analysis: models.ProblemAnalysis) -> str:
        tag_keys = models.ProblemAnalysisTag.objects.filter(**{
            models.ProblemAnalysisTag.field_name.ANALYSIS: analysis,
        }).select_related(
            models.ProblemAnalysisTag.field_name.TAG,
        ).values_list(
            models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.KEY,
            flat=True,
        )
        return ', '.join(tag_keys)

    @admin.display(description='Hint steps')
    def get_hint_steps(self, obj: models.ProblemAnalysis) -> int:
        return len(obj.hint)
