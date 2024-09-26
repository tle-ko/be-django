from django.contrib import admin

from apps.crews.proxy import Crew

from . import models


@admin.register(models.CrewActivityDAO)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewActivityDAO.field_name.CREW,
        models.CrewActivityDAO.field_name.NAME,
        models.CrewActivityDAO.field_name.START_AT,
        models.CrewActivityDAO.field_name.END_AT,
        'nth',
        'is_in_progress',
        'has_started',
        'has_ended',
    ]
    search_fields = [
        models.CrewActivityDAO.field_name.CREW+'__'+Crew.field_name.NAME,
        models.CrewActivityDAO.field_name.NAME,
    ]

    @admin.display(description='회차 번호')
    def nth(self, obj: models.CrewActivityDAO) -> int:
        for nth, activity in enumerate(models.CrewActivityDAO.objects.filter(crew=obj.crew), start=1):
            if activity == obj:
                return nth

    @admin.display(boolean=True, description='진행 중')
    def is_in_progress(self, obj: models.CrewActivityDAO) -> bool:
        return obj.is_in_progress()

    @admin.display(boolean=True, description='시작 됨')
    def has_started(self, obj: models.CrewActivityDAO) -> bool:
        return obj.has_started()

    @admin.display(boolean=True, description='종료 됨')
    def has_ended(self, obj: models.CrewActivityDAO) -> bool:
        return obj.has_ended()


@admin.register(models.CrewActivityProblemDAO)
class CrewActivityProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.CrewActivityProblemDAO.field_name.CREW,
        models.CrewActivityProblemDAO.field_name.ACTIVITY,
        models.CrewActivityProblemDAO.field_name.PROBLEM,
        models.CrewActivityProblemDAO.field_name.ORDER,
    ]
    search_fields = [
        models.CrewActivityProblemDAO.field_name.CREW+'__'+Crew.field_name.NAME,
        models.CrewActivityProblemDAO.field_name.ACTIVITY+'__'+models.CrewActivityDAO.field_name.NAME,
        models.CrewActivityProblemDAO.field_name.PROBLEM+'__'+models.Problem.field_name.TITLE,
    ]
