from django.contrib import admin

from problems import models


@admin.register(models.ProblemAnalysisTag)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysisTag.field_name.ANALYSIS,
        models.ProblemAnalysisTag.field_name.TAG,
    ]
    search_fields = [
        models.ProblemAnalysisTag.field_name.ANALYSIS+'__' +
        models.ProblemAnalysis.field_name.PROBLEM+'__'+models.Problem.field_name.TITLE,
        models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.KEY,
        models.ProblemAnalysisTag.field_name.TAG +
        '__'+models.ProblemTag.field_name.NAME_KO,
        models.ProblemAnalysisTag.field_name.TAG +
        '__'+models.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [models.ProblemAnalysisTag.field_name.ANALYSIS]
