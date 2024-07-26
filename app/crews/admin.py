from django.contrib import admin

from crews.models import (
    Crew,
    CrewActivity,
    CrewActivityProblem,
    CrewApplicant,
    CrewMember,
    CrewSubmittableLanguage,
)
from users.models import User


admin.site.register([
    CrewActivityProblem,
    CrewApplicant,
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
    def get_display_name(self, crew: Crew):
        return f'{crew.icon} {crew.name}'

    @admin.display(description='Captain')
    def get_captain(self, obj: Crew):
        return CrewMember.objects.get(**{
            CrewMember.field_name.CREW: obj,
            CrewMember.field_name.IS_CAPTAIN: True,
        })

    @admin.display(description='Members')
    def get_members(self, crew: Crew):
        members_count = CrewMember.objects.filter(**{
            CrewMember.field_name.CREW: crew,
        }).count()
        return f'{members_count} / {crew.max_members}'

    @admin.display(description='Applicants')
    def get_applicants(self, obj: Crew):
        return CrewApplicant.objects.filter(**{
            CrewApplicant.field_name.CREW: obj,
        }).count()

    @admin.display(description='Activities')
    def get_activities(self, obj: Crew):
        return CrewActivity.objects.filter(**{
            CrewActivity.field_name.CREW: obj,
        }).count()


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


@admin.register(CrewSubmittableLanguage)
class CrewSubmittableLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        CrewSubmittableLanguage.field_name.CREW,
        CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    search_fields = [
        CrewActivity.field_name.CREW+'__'+Crew.field_name.NAME,
        CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    ordering = [
        CrewSubmittableLanguage.field_name.CREW,
        CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
