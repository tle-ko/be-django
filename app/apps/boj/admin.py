from django.contrib import admin
from django.db.models import QuerySet

from . import proxy


@admin.register(proxy.BOJUser)
class BOJUserModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.BOJUser.field_name.USERNAME,
        proxy.BOJUser.field_name.LEVEL,
        proxy.BOJUser.field_name.RATING,
        proxy.BOJUser.field_name.UPDATED_AT,
    ]
    actions = [
        'update',
        'schedule_update',
    ]

    @admin.action(description="Schedule update selected BOJ user data. (via solved.ac API)")
    def schedule_update(self, request, queryset: QuerySet[proxy.BOJUser]):
        for obj in queryset:
            obj.schedule_update()

    @admin.action(description="Update selected BOJ user data right now. (via solved.ac API)")
    def update(self, request, queryset: QuerySet[proxy.BOJUser]):
        for obj in queryset:
            obj.update()


@admin.register(proxy.BOJUserSnapshot)
class BOJUserSnapshotModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.BOJUserSnapshot.field_name.USER,
        proxy.BOJUserSnapshot.field_name.LEVEL,
        proxy.BOJUserSnapshot.field_name.RATING,
        proxy.BOJUserSnapshot.field_name.CREATED_AT,
    ]
