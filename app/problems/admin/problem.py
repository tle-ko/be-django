from django.contrib import admin
from django.db.models import QuerySet

from problems import models
from problems import services
from users.models import User


@admin.register(models.Problem)
class ProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.Problem.field_name.TITLE,
        models.Problem.field_name.CREATED_BY,
        models.Problem.field_name.CREATED_AT,
        models.Problem.field_name.UPDATED_AT,
    ]
    search_fields = [
        models.Problem.field_name.TITLE,
        models.Problem.field_name.CREATED_BY+'__'+User.field_name.USERNAME,
    ]
    ordering = ['-'+models.Problem.field_name.CREATED_AT]
    actions = [
        'analyze',
    ]

    @admin.action(description="Analyze selected problems.")
    def analyze(self, request, queryset: QuerySet[models.Problem]):
        for obj in queryset:
            service = services.get_problem_service(obj)
            service.analyze()
