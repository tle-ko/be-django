from django.contrib import admin

from apps.problems.proxy import Problem

from . import proxy


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
        proxy.ProblemAnalysis.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
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
            proxy.ProblemAnalysisTag.field_name.TAG+'__'+proxy.ProblemTag.field_name.KEY,
            flat=True,
        )
        return ', '.join(tag_keys)

    @admin.display(description='Hint steps')
    def get_hint_steps(self, obj: proxy.ProblemAnalysis) -> int:
        return len(obj.hint)


@admin.register(proxy.ProblemAnalysisTag)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.ProblemAnalysisTag.field_name.ANALYSIS,
        proxy.ProblemAnalysisTag.field_name.TAG,
    ]
    search_fields = [
        proxy.ProblemAnalysisTag.field_name.ANALYSIS+'__'+proxy.ProblemAnalysis.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
        proxy.ProblemAnalysisTag.field_name.TAG+'__'+proxy.ProblemTag.field_name.KEY,
        proxy.ProblemAnalysisTag.field_name.TAG+'__'+proxy.ProblemTag.field_name.NAME_KO,
        proxy.ProblemAnalysisTag.field_name.TAG+'__'+proxy.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [proxy.ProblemAnalysisTag.field_name.ANALYSIS]


@admin.register(proxy.ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.ProblemTag.field_name.KEY,
        proxy.ProblemTag.field_name.NAME_KO,
        proxy.ProblemTag.field_name.NAME_EN,
    ]
    search_fields = [
        proxy.ProblemTag.field_name.KEY,
        proxy.ProblemTag.field_name.NAME_KO,
        proxy.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [proxy.ProblemTag.field_name.KEY]


@admin.register(proxy.ProblemTagRelation)
class ProblemTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.ProblemTagRelation.field_name.PARENT,
        proxy.ProblemTagRelation.field_name.CHILD,
    ]
    search_fields = [
        proxy.ProblemTagRelation.field_name.PARENT,
        proxy.ProblemTagRelation.field_name.CHILD,
    ]
    ordering = [proxy.ProblemTagRelation.field_name.PARENT]
