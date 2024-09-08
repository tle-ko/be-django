from django.contrib import admin

from apps.problems.models import Problem
from apps.analyses.models import ProblemAnalysis
from apps.analyses.models import ProblemAnalysisTag
from apps.analyses.models import ProblemTag
from apps.analyses.models import ProblemTagRelation


@admin.register(ProblemAnalysis)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemAnalysis.field_name.PROBLEM,
        ProblemAnalysis.field_name.DIFFICULTY,
        'get_time_complexity',
        'get_tags',
        'get_hint_steps',
        ProblemAnalysis.field_name.CREATED_AT,
    ]
    search_fields = [
        ProblemAnalysis.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
        ProblemAnalysis.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+ProblemAnalysis.field_name.CREATED_AT]

    @admin.display(description='Time complexity')
    def get_time_complexity(self, obj: ProblemAnalysis) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, analysis: ProblemAnalysis) -> str:
        tag_keys = ProblemAnalysisTag.objects.filter(**{
            ProblemAnalysisTag.field_name.ANALYSIS: analysis,
        }).select_related(
            ProblemAnalysisTag.field_name.TAG,
        ).values_list(
            ProblemAnalysisTag.field_name.TAG+'__'+ProblemTag.field_name.KEY,
            flat=True,
        )
        return ', '.join(tag_keys)

    @admin.display(description='Hint steps')
    def get_hint_steps(self, obj: ProblemAnalysis) -> int:
        return len(obj.hint)


@admin.register(ProblemAnalysisTag)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemAnalysisTag.field_name.ANALYSIS,
        ProblemAnalysisTag.field_name.TAG,
    ]
    search_fields = [
        ProblemAnalysisTag.field_name.ANALYSIS+'__'+ProblemAnalysis.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
        ProblemAnalysisTag.field_name.TAG+'__'+ProblemTag.field_name.KEY,
        ProblemAnalysisTag.field_name.TAG+'__'+ProblemTag.field_name.NAME_KO,
        ProblemAnalysisTag.field_name.TAG+'__'+ProblemTag.field_name.NAME_EN,
    ]
    ordering = [ProblemAnalysisTag.field_name.ANALYSIS]


@admin.register(ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemTag.field_name.KEY,
        ProblemTag.field_name.NAME_KO,
        ProblemTag.field_name.NAME_EN,
    ]
    search_fields = [
        ProblemTag.field_name.KEY,
        ProblemTag.field_name.NAME_KO,
        ProblemTag.field_name.NAME_EN,
    ]
    ordering = [ProblemTag.field_name.KEY]


@admin.register(ProblemTagRelation)
class ProblemTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemTagRelation.field_name.PARENT,
        ProblemTagRelation.field_name.CHILD,
    ]
    search_fields = [
        ProblemTagRelation.field_name.PARENT,
        ProblemTagRelation.field_name.CHILD,
    ]
    ordering = [ProblemTagRelation.field_name.PARENT]
