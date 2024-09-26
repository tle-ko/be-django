from django.contrib import admin

from apps.crews.proxy import Crew

from . import proxy


admin.site.register([
    proxy.CrewActivityProblem,
])


@admin.register(proxy.CrewActivity)
class CrewActivityModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.CrewActivity.field_name.CREW,
        proxy.CrewActivity.field_name.NAME,
        proxy.CrewActivity.field_name.START_AT,
        proxy.CrewActivity.field_name.END_AT,
        'nth',
        'is_in_progress',
        'has_started',
        'has_ended',
    ]
    search_fields = [
        proxy.CrewActivity.field_name.CREW+'__'+Crew.field_name.NAME,
        proxy.CrewActivity.field_name.NAME,
    ]

    @admin.display(description='회차 번호')
    def nth(self, obj: proxy.CrewActivity) -> int:
        for nth, activity in enumerate(proxy.CrewActivity.objects.filter(crew=obj.crew), start=1):
            if activity == obj:
                return nth

    @admin.display(boolean=True, description='진행 중')
    def is_in_progress(self, obj: proxy.CrewActivity) -> bool:
        return obj.is_in_progress()

    @admin.display(boolean=True, description='시작 됨')
    def has_started(self, obj: proxy.CrewActivity) -> bool:
        return obj.has_started()

    @admin.display(boolean=True, description='종료 됨')
    def has_ended(self, obj: proxy.CrewActivity) -> bool:
        return obj.has_ended()
