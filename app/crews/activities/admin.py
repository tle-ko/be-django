from django.contrib import admin

from crews.models import Crew
from crews.activities.models import CrewActivity
from crews.activities.models import CrewActivityProblem
from crews.activities.models import CrewActivitySubmission


admin.site.register([
    CrewActivityProblem,
    CrewActivitySubmission,
])


@admin.register(CrewActivity)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        CrewActivity.field_name.CREW,
        CrewActivity.field_name.NAME,
        CrewActivity.field_name.START_AT,
        CrewActivity.field_name.END_AT,
        'nth',
        'is_in_progress',
        'has_started',
        'has_ended',
    ]
    search_fields = [
        CrewActivity.field_name.CREW+'__'+Crew.field_name.NAME,
        CrewActivity.field_name.NAME,
    ]

    @admin.display(description='회차 번호')
    def nth(self, obj: CrewActivity) -> int:
        for nth, activity in enumerate(CrewActivity.objects.filter(crew=obj.crew), start=1):
            if activity == obj:
                return nth

    @admin.display(boolean=True, description='진행 중')
    def is_in_progress(self, obj: CrewActivity) -> bool:
        return obj.is_in_progress()

    @admin.display(boolean=True, description='시작 됨')
    def has_started(self, obj: CrewActivity) -> bool:
        return obj.has_started()

    @admin.display(boolean=True, description='종료 됨')
    def has_ended(self, obj: CrewActivity) -> bool:
        return obj.has_ended()
