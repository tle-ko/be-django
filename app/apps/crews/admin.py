from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from users.models import User

from . import models


@admin.register(models.CrewDAO)
class CrewModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewDAO.method_name.GET_DISPLAY_NAME,
        models.CrewDAO.field_name.PK,
        models.CrewDAO.field_name.IS_ACTIVE,
        models.CrewDAO.field_name.IS_RECRUITING,
        models.CrewDAO.field_name.CREATED_AT,
    ]
    search_fields = [
        models.CrewDAO.field_name.NAME,
        models.CrewDAO.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
        models.CrewDAO.field_name.ICON,
    ]


@admin.register(models.CrewMemberDAO)
class CrewMemberModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewMemberDAO.field_name.USER,
        models.CrewMemberDAO.field_name.CREW,
        models.CrewMemberDAO.field_name.IS_CAPTAIN,
        models.CrewMemberDAO.field_name.CREATED_AT,
    ]
    search_fields = [
        models.CrewMemberDAO.field_name.CREW+'__'+models.CrewDAO.field_name.NAME,
        models.CrewMemberDAO.field_name.USER+'__'+User.field_name.USERNAME,
    ]
    ordering = [
        models.CrewMemberDAO.field_name.CREW,
        models.CrewMemberDAO.field_name.IS_CAPTAIN,
    ]


@admin.register(models.CrewSubmittableLanguageDAO)
class CrewSubmittableLanguageModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewSubmittableLanguageDAO.field_name.CREW,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]
    search_fields = [
        models.CrewSubmittableLanguageDAO.field_name.CREW +
        '__'+models.CrewDAO.field_name.NAME,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]
    ordering = [
        models.CrewSubmittableLanguageDAO.field_name.CREW,
        models.CrewSubmittableLanguageDAO.field_name.LANGUAGE,
    ]


@admin.register(models.CrewApplicationDAO)
class CrewApplicantModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewApplicationDAO.field_name.CREW,
        models.CrewApplicationDAO.field_name.APPLICANT,
        models.CrewApplicationDAO.field_name.IS_ACCEPTED,
        models.CrewApplicationDAO.field_name.IS_PENDING,
        models.CrewApplicationDAO.field_name.REVIEWED_BY,
    ]
    actions = [
        'accept',
        'reject',
        'send_on_create_notification',
        'send_on_accept_notification',
        'send_on_reject_notification',
    ]

    @admin.action(description="Accept user")
    def accept(self, request: HttpRequest, queryset: QuerySet[models.CrewApplicationDAO]):
        for obj in queryset:
            obj.accept(request.user)

    @admin.action(description="Reject user")
    def reject(self, request: HttpRequest, queryset: QuerySet[models.CrewApplicationDAO]):
        for obj in queryset:
            obj.reject(request.user)

    @admin.display(description='Send On Create Notification')
    def send_on_create_notification(self, request, queryset: QuerySet[models.CrewApplicationDAO]):
        for obj in queryset:
            obj.send_on_create_notification()

    @admin.display(description='Send On Accept Notification')
    def send_on_accept_notification(self, request, queryset: QuerySet[models.CrewApplicationDAO]):
        for obj in queryset:
            obj.send_on_accept_notification()

    @admin.display(description='Send On Reject Notification')
    def send_on_reject_notification(self, request, queryset: QuerySet[models.CrewApplicationDAO]):
        for obj in queryset:
            obj.send_on_reject_notification()


@admin.register(models.CrewActivityDAO)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewActivityDAO.field_name.CREW,
        models.CrewActivityDAO.field_name.NAME,
        models.CrewActivityDAO.field_name.START_AT,
        models.CrewActivityDAO.field_name.END_AT,
        'nth',
        models.CrewActivityDAO.method_name.IS_IN_PROGRESS,
        models.CrewActivityDAO.method_name.HAS_STARTED,
        models.CrewActivityDAO.method_name.HAS_ENDED,
    ]
    search_fields = [
        models.CrewActivityDAO.field_name.CREW+'__'+models.CrewDAO.field_name.NAME,
        models.CrewActivityDAO.field_name.NAME,
    ]

    @admin.display(description='회차 번호')
    def nth(self, obj: models.CrewActivityDAO) -> int:
        for nth, activity in enumerate(models.CrewActivityDAO.objects.filter(crew=obj.crew), start=1):
            if activity == obj:
                return nth


@admin.register(models.CrewProblemDAO)
class CrewActivityProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewProblemDAO.field_name.CREW,
        models.CrewProblemDAO.field_name.ACTIVITY,
        models.CrewProblemDAO.field_name.PROBLEM,
        models.CrewProblemDAO.field_name.ORDER,
    ]
    search_fields = [
        models.CrewProblemDAO.field_name.CREW+'__'+models.CrewDAO.field_name.NAME,
        models.CrewProblemDAO.field_name.ACTIVITY+'__'+models.CrewActivityDAO.field_name.NAME,
        models.CrewProblemDAO.field_name.PROBLEM+'__'+models.ProblemDAO.field_name.TITLE,
    ]
