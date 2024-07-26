from textwrap import shorten

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.utils.translation import ngettext

from problems.models import (
    Problem,
    ProblemAnalysis,
    ProblemAnalysisQueue,
    ProblemTag,
)
from problems.services.analysis import AnalysingService
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
        'analyze',
        'add_to_analysis_queue',
        'set_creator',
    ]

    @admin.action(description="Set admin(you) as creator for selected problems")
    def set_creator(self, request, queryset: QuerySet[Problem]):
        updated = queryset.update(**{
            Problem.field_name.CREATED_BY: request.user,
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

    @admin.action(description="Add selected problems to analysis queue")
    def add_to_analysis_queue(self, request, queryset: QuerySet[Problem]):
        for problem in queryset:
            ProblemAnalysisQueue.objects.create(**{
                ProblemAnalysisQueue.field_name.PROBLEM: problem,
            })
        self.message_user(
            request,
            ngettext(
                "%d problem was successfully added to analysis queue.",
                "%d problems were successfully added to analysis queue.",
                queryset.count(),
            )
            % queryset.count(),
            messages.SUCCESS,
        )

    @admin.action(description="Analyze selected problems")
    def analyze(self, request, queryset: QuerySet[Problem]):
        analysing_service = AnalysingService.get_instance()
        for problem in queryset:
            analysis = analysing_service.analyze(problem)
            analysis.save()
        self.message_user(
            request,
            ngettext(
                "%d problem was successfully analyzed.",
                "%d problems were successfully analyzed.",
                queryset.count(),
            )
            % queryset.count(),
            messages.SUCCESS,
        )


@admin.register(ProblemAnalysis)
class ProblemAnalysisModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemAnalysis.field_name.PROBLEM,
        ProblemAnalysis.field_name.DIFFICULTY,
        'get_timecomplexity',
        'get_tags',
        'get_hint',
        ProblemAnalysis.field_name.CREATED_AT,
    ]
    search_fields = [
        ProblemAnalysis.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
        ProblemAnalysis.field_name.TIME_COMPLEXITY,
    ]
    ordering = ['-'+ProblemAnalysis.field_name.CREATED_AT]

    @admin.display(description='Big-O')
    def get_timecomplexity(self, obj: ProblemAnalysis) -> str:
        return f'O({obj.time_complexity})'

    @admin.display(description='Tags')
    def get_tags(self, obj: ProblemAnalysis) -> str:
        def get_tag_keys():
            for tag in obj.tags.all():
                yield f'#{tag.key}'
        return ' '.join(get_tag_keys())

    @admin.display(description='Hint (Steps, Verbose)')
    def get_hint(self, obj: ProblemAnalysis) -> str:
        hints_in_a_row = ', '.join(obj.hint)
        return len(obj.hint), shorten(hints_in_a_row, width=32)


@admin.register(ProblemAnalysisQueue)
class ProblemAnalysisQueueModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemAnalysisQueue.field_name.PROBLEM,
        ProblemAnalysisQueue.field_name.ANALYSIS,
        ProblemAnalysisQueue.field_name.IS_ANALYZING,
        'get_is_analyzed',
        ProblemAnalysisQueue.field_name.CREATED_AT,
    ]
    search_fields = [
        ProblemAnalysisQueue.field_name.PROBLEM+'__'+Problem.field_name.TITLE,
    ]
    ordering = [
        ProblemAnalysisQueue.field_name.CREATED_AT,
    ]

    @admin.display(description='Is analyzed', boolean=True)
    def get_is_analyzed(self, obj: ProblemAnalysisQueue) -> bool:
        return obj.analysis is not None


@admin.register(ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = [
        ProblemTag.field_name.KEY,
        ProblemTag.field_name.NAME_KO,
        ProblemTag.field_name.NAME_EN,
        ProblemTag.field_name.PARENT,
    ]
    search_fields = [
        ProblemTag.field_name.KEY,
        ProblemTag.field_name.NAME_KO,
        ProblemTag.field_name.NAME_EN,
    ]
    ordering = [ProblemTag.field_name.KEY]
