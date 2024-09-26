from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from . import proxy


@admin.register(proxy.CrewApplication)
class CrewApplicantModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.CrewApplication.field_name.CREW,
        proxy.CrewApplication.field_name.APPLICANT,
        proxy.CrewApplication.field_name.IS_ACCEPTED,
        proxy.CrewApplication.field_name.IS_PENDING,
        proxy.CrewApplication.field_name.REVIEWED_BY,
    ]
    actions = [
        'accept',
        'reject',
    ]

    @admin.action(description="Accept user")
    def accept(self, request: HttpRequest, queryset: QuerySet[proxy.CrewApplication]):
        for obj in queryset:
            obj.accept(request.user)

    @admin.action(description="Reject user")
    def reject(self, request: HttpRequest, queryset: QuerySet[proxy.CrewApplication]):
        for obj in queryset:
            obj.reject(request.user)
