from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from apps.crews.applications.models import CrewApplication
from apps.crews.applications.services import accept
from apps.crews.applications.services import reject


@admin.register(CrewApplication)
class CrewApplicantModelAdmin(admin.ModelAdmin):
    list_display = [
        CrewApplication.field_name.CREW,
        CrewApplication.field_name.APPLICANT,
        CrewApplication.field_name.IS_ACCEPTED,
        CrewApplication.field_name.IS_PENDING,
        CrewApplication.field_name.REVIEWED_BY,
    ]
    actions = [
        'accept',
        'reject',
    ]

    @admin.action(description="Accept user")
    def accept(self, request: HttpRequest, queryset: QuerySet[CrewApplication]):
        for applicant in queryset:
            accept(applicant, request.user)

    @admin.action(description="Reject user")
    def reject(self, request: HttpRequest, queryset: QuerySet[CrewApplication]):
        for applicant in queryset:
            reject(applicant, request.user)
