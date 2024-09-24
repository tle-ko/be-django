from django.contrib import admin

from apps.activities.proxy import CrewActivity
from apps.applications.proxy import CrewApplication
from users.models import User

from . import proxy


@admin.register(proxy.Crew)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'get_display_name',
        'get_captain',
        'get_members',
        'get_applicants',
        'get_activities',
        proxy.Crew.field_name.IS_ACTIVE,
        proxy.Crew.field_name.IS_RECRUITING,
        proxy.Crew.field_name.CREATED_AT,
    ]
    search_fields = [
        proxy.Crew.field_name.NAME,
        proxy.Crew.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
        proxy.Crew.field_name.ICON,
    ]

    @admin.display(description='Display Name')
    def get_display_name(self, obj: proxy.Crew):
        return obj.display_name()

    @admin.display(description='Captain')
    def get_captain(self, obj: proxy.Crew):
        return proxy.CrewMember.objects.filter(crew=obj, is_captain=True).get()

    @admin.display(description='Members')
    def get_members(self, obj: proxy.Crew):
        return f'{proxy.CrewMember.objects.filter(crew=obj).count()} / {obj.max_members}'

    @admin.display(description='Applicants')
    def get_applicants(self, obj: proxy.Crew):
        return CrewApplication.objects.filter(crew=obj).count()

    @admin.display(description='Activities')
    def get_activities(self, obj: proxy.Crew):
        return CrewActivity.objects.filter(crew=obj).count()


@admin.register(proxy.CrewMember)
class CrewMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.CrewMember.field_name.USER,
        proxy.CrewMember.field_name.CREW,
        proxy.CrewMember.field_name.IS_CAPTAIN,
        proxy.CrewMember.field_name.CREATED_AT,
    ]
    search_fields = [
        proxy.CrewMember.field_name.CREW+'__'+proxy.Crew.field_name.NAME,
        proxy.CrewMember.field_name.USER+'__'+User.field_name.USERNAME,
    ]
    ordering = [
        proxy.CrewMember.field_name.CREW,
        proxy.CrewMember.field_name.IS_CAPTAIN,
    ]


@admin.register(proxy.CrewSubmittableLanguage)
class CrewSubmittableLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.CrewSubmittableLanguage.field_name.CREW,
        proxy.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    search_fields = [
        CrewActivity.field_name.CREW+'__'+proxy.Crew.field_name.NAME,
        proxy.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    ordering = [
        proxy.CrewSubmittableLanguage.field_name.CREW,
        proxy.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
