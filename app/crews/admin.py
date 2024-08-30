from django.contrib import admin

from crews.activities.models import CrewActivity
from crews.applications.models import CrewApplication
from crews.models import Crew
from crews.models import CrewMember
from crews.models import CrewSubmittableLanguage
from users.models import User


@admin.register(Crew)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
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
    def get_display_name(self, obj: Crew):
        return obj.display_name()

    @admin.display(description='Captain')
    def get_captain(self, obj: Crew):
        return CrewMember.objects.filter(crew=obj, is_captain=True).get()

    @admin.display(description='Members')
    def get_members(self, obj: Crew):
        return f'{CrewMember.objects.filter(crew=obj).count()} / {obj.max_members}'

    @admin.display(description='Applicants')
    def get_applicants(self, obj: Crew):
        return CrewApplication.objects.crew(obj).count()

    @admin.display(description='Activities')
    def get_activities(self, obj: Crew):
        return CrewActivity.objects.crew(obj).count()


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
