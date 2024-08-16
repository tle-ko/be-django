from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from crews import models
from crews import services
from users.models import User


admin.site.register([
    models.CrewActivityProblem,
])


@admin.register(models.Crew)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        'get_display_name',
        'get_captain',
        'get_members',
        'get_applicants',
        'get_activities',
        models.Crew.field_name.IS_ACTIVE,
        models.Crew.field_name.IS_RECRUITING,
        models.Crew.field_name.CREATED_AT,
    ]
    search_fields = [
        models.Crew.field_name.NAME,
        models.Crew.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
        models.Crew.field_name.ICON,
    ]

    @admin.display(description='Display Name')
    def get_display_name(self, crew: models.Crew):
        return f'{crew.icon} {crew.name}'

    @admin.display(description='Captain')
    def get_captain(self, obj: models.Crew):
        return models.CrewMember.objects.get(**{
            models.CrewMember.field_name.CREW: obj,
            models.CrewMember.field_name.IS_CAPTAIN: True,
        })

    @admin.display(description='Members')
    def get_members(self, crew: models.Crew):
        members_count = models.CrewMember.objects.filter(**{
            models.CrewMember.field_name.CREW: crew,
        }).count()
        return f'{members_count} / {crew.max_members}'

    @admin.display(description='Applicants')
    def get_applicants(self, obj: models.Crew):
        return models.CrewApplicant.objects.filter(**{
            models.CrewApplicant.field_name.CREW: obj,
        }).count()

    @admin.display(description='Activities')
    def get_activities(self, obj: models.Crew):
        return models.CrewActivity.objects.filter(**{
            models.CrewActivity.field_name.CREW: obj,
        }).count()


@admin.register(models.CrewMember)
class CrewMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewMember.field_name.USER,
        models.CrewMember.field_name.CREW,
        models.CrewMember.field_name.IS_CAPTAIN,
        models.CrewMember.field_name.CREATED_AT,
    ]
    search_fields = [
        models.CrewMember.field_name.CREW+'__'+models.Crew.field_name.NAME,
        models.CrewMember.field_name.USER+'__'+User.field_name.USERNAME,
    ]
    ordering = [
        models.CrewMember.field_name.CREW,
        models.CrewMember.field_name.IS_CAPTAIN,
    ]


@admin.register(models.CrewActivity)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewActivity.field_name.CREW,
        models.CrewActivity.field_name.NAME,
        models.CrewActivity.field_name.START_AT,
        models.CrewActivity.field_name.END_AT,
        'nth',
        'is_opened',
        'is_closed',
    ]
    search_fields = [
        models.CrewActivity.field_name.CREW+'__'+models.Crew.field_name.NAME,
        models.CrewActivity.field_name.NAME,
    ]

    @admin.display(boolean=True, description='Is Opened')
    def is_opened(self, obj: models.CrewActivity) -> bool:
        return services.crew_acitivity.is_opened(obj)

    @admin.display(boolean=True, description='Is Closed')
    def is_closed(self, obj: models.CrewActivity) -> bool:
        return services.crew_acitivity.is_closed(obj)

    @admin.display(description='N-th')
    def nth(self, obj: models.CrewActivity) -> int:
        return services.crew_acitivity.number(obj)


@admin.register(models.CrewSubmittableLanguage)
class CrewSubmittableLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewSubmittableLanguage.field_name.CREW,
        models.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    search_fields = [
        models.CrewActivity.field_name.CREW+'__'+models.Crew.field_name.NAME,
        models.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]
    ordering = [
        models.CrewSubmittableLanguage.field_name.CREW,
        models.CrewSubmittableLanguage.field_name.LANGUAGE,
    ]


@admin.register(models.CrewApplicant)
class CrewApplicantModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewApplicant.field_name.CREW,
        models.CrewApplicant.field_name.USER,
        models.CrewApplicant.field_name.IS_ACCEPTED,
        models.CrewApplicant.field_name.REVIEWED_BY,
    ]
    actions = [
        'accept',
        'reject',
    ]

    @admin.action(description="Accept user")
    def accept(self, request: HttpRequest, queryset: QuerySet[models.CrewApplicant]):
        for applicant in queryset:
            services.crew_applicant.accept(applicant, request.user)
            services.crew_applicant.notify_accepted(applicant)

    @admin.action(description="Reject user")
    def reject(self, request: HttpRequest, queryset: QuerySet[models.CrewApplicant]):
        for applicant in queryset:
            services.crew_applicant.reject(applicant, request.user)
            services.crew_applicant.notify_rejected(applicant)
