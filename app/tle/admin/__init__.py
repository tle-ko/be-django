from django.contrib import admin

from users.models import User
from tle.models import *


admin.site.register([
    CrewActivityProblem,
    CrewApplicant,
    Submission,
    SubmissionComment,
])

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
