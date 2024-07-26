from textwrap import shorten

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.utils.translation import ngettext

from users.models import User
from tle.models import *


admin.site.register([
    CrewActivityProblem,
    CrewApplicant,
    Submission,
    SubmissionComment,
])



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
        'set_creator',
        'add_to_analysis_queue',
    ]

    @admin.action(description="set admin(you) as creator for selected problems")
    def set_creator(self, request, queryset: QuerySet[Problem]):
        updated = queryset.update(created_by=request.user)
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

    @admin.action(description="add selected problems to analysis queue")
    def add_to_analysis_queue(self, request, queryset: QuerySet[Problem]):
        ProblemAnalysisQueue.extend(queryset)
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
        return len(obj.hint), shorten(', '.join(obj.hint), width=32)


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

    @admin.display(description='Is Analyzed', boolean=True)
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


@admin.register(Crew)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        'get_display_name',
        'get_captain',
        'get_members',
        'get_applicants',
        'get_activities',
        Crew.field_name.IS_ACTIVE,
        Crew.field_name.IS_RECRUITING,
        Crew.field_name.CREATED_AT,
    ]
    search_fields = [
        Crew.field_name.NAME,
        Crew.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
        Crew.field_name.ICON,
    ]

    @admin.display(description='Display Name')
    def get_display_name(self, obj: Crew) -> str:
        return obj.get_display_name()

    @admin.display(description='Captain')
    def get_captain(self, obj: Crew) -> str:
        return obj.get_captain()

    @admin.display(description='Members')
    def get_members(self, obj: Crew) -> str:
        return f'{obj.members.count()} / {obj.max_members}'

    @admin.display(description='Applicants')
    def get_applicants(self, obj: Crew) -> str:
        return obj.applicants.count()

    @admin.display(description='Activities')
    def get_activities(self, obj: Crew) -> str:
        return obj.activities.count()


@admin.register(CrewMember)
class CrewMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        CrewMember.field_name.USER,
        CrewMember.field_name.CREW,
        CrewMember.field_name.IS_CAPTAIN,
        CrewMember.field_name.CREATED_AT,
    ]
    search_fields = [
        CrewMember.field_name.CREW+'__'+Crew.field_name.NAME,
        CrewMember.field_name.USER+'__'+User.field_name.USERNAME,
    ]
    ordering = [
        CrewMember.field_name.CREW,
        CrewMember.field_name.IS_CAPTAIN,
    ]


@admin.register(CrewActivity)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        CrewActivity.field_name.CREW,
        CrewActivity.field_name.NAME,
        CrewActivity.field_name.START_AT,
        CrewActivity.field_name.END_AT,
        'nth',
        'is_opened',
        'is_closed',
    ]
    search_fields = [
        CrewActivity.field_name.CREW+'__'+Crew.field_name.NAME,
        CrewActivity.field_name.NAME,
    ]


@admin.register(SubmissionLanguage)
class SubmissionLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        SubmissionLanguage.field_name.KEY,
        SubmissionLanguage.field_name.NAME,
        SubmissionLanguage.field_name.EXTENSION,
    ]
    search_fields = [
        SubmissionLanguage.field_name.KEY,
        SubmissionLanguage.field_name.NAME,
        SubmissionLanguage.field_name.EXTENSION,
    ]
