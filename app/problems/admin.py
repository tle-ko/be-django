from textwrap import shorten

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.utils.translation import ngettext

from problems import models
from users.models import User


@admin.register(models.Problem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.Problem.field_name.TITLE,
        models.Problem.field_name.CREATED_BY,
        models.Problem.field_name.CREATED_AT,
        models.Problem.field_name.UPDATED_AT,
    ]
    search_fields = [
        models.Problem.field_name.TITLE,
        models.Problem.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
    ]
    ordering = ['-'+models.Problem.field_name.CREATED_AT]
    actions = [
        'analyze',
        'add_to_analysis_queue',
        'set_creator',
    ]

    @admin.action(description="Set admin(you) as creator for selected problems")
    def set_creator(self, request, queryset: QuerySet[models.Problem]):
        updated = queryset.update(**{
            models.Problem.field_name.CREATED_BY: request.user,
        })
        self.message_user(
            request,
            ngettext(
                "%d problem was successfully updated.",
                "%d problems were successfully updated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(models.ProblemAnalysis)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysis.field_name.PROBLEM,
        models.ProblemAnalysis.field_name.DIFFICULTY,
        'get_timecomplexity',
        'get_tags',
        'get_hint',
        models.ProblemAnalysis.field_name.CREATED_AT,
    ]
    search_fields = [
        models.ProblemAnalysis.field_name.PROBLEM+'__'+models.Problem.field_name.TITLE,
        models.ProblemAnalysis.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+models.ProblemAnalysis.field_name.CREATED_AT]

    @admin.display(description='Big-O')
    def get_timecomplexity(self, obj: models.ProblemAnalysis) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, analysis: models.ProblemAnalysis) -> str:
        tags = models.ProblemAnalysisTag.objects.filter(**{
            models.ProblemAnalysisTag.field_name.ANALYSIS: analysis,
        }).values_list(models.ProblemAnalysisTag.field_name.TAG, flat=True)
        return ' '.join(tag.key for tag in tags)

    @admin.display(description='Hint (Steps, Verbose)')
    def get_hint(self, obj: models.ProblemAnalysis) -> str:
        hints_in_a_row = ', '.join(obj.hint)
        return len(obj.hint), shorten(hints_in_a_row, width=32)


@admin.register(models.ProblemAnalysisTag)
class ProblemAnalysisTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemAnalysisTag.field_name.ANALYSIS,
        models.ProblemAnalysisTag.field_name.TAG,
    ]
    search_fields = [
        models.ProblemAnalysisTag.field_name.ANALYSIS+'__'+models.ProblemAnalysis.field_name.PROBLEM+'__'+models.Problem.field_name.TITLE,
        models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.KEY,
        models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.NAME_KO,
        models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [models.ProblemAnalysisTag.field_name.ANALYSIS]


@admin.register(models.ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemTag.field_name.KEY,
        models.ProblemTag.field_name.NAME_KO,
        models.ProblemTag.field_name.NAME_EN,
    ]
    search_fields = [
        models.ProblemTag.field_name.KEY,
        models.ProblemTag.field_name.NAME_KO,
        models.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [models.ProblemTag.field_name.KEY]


@admin.register(models.ProblemTagRelation)
class ProblemTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemTagRelation.field_name.PARENT,
        models.ProblemTagRelation.field_name.CHILD,
    ]
    search_fields = [
        models.ProblemTagRelation.field_name.PARENT,
        models.ProblemTagRelation.field_name.CHILD,
    ]
    ordering = [models.ProblemTagRelation.field_name.PARENT]
