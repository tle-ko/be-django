from django.contrib import admin
from django.db.models import QuerySet

from . import models


@admin.register(models.BOJUser)
class BOJUserModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUser.field_name.USERNAME,
        models.BOJUser.field_name.LEVEL,
        models.BOJUser.field_name.RATING,
        models.BOJUser.field_name.UPDATED_AT,
    ]
    actions = [
        'update',
        'schedule_update',
    ]

    @admin.action(description="Schedule update selected BOJ user data. (via solved.ac API)")
    def schedule_update(self, request, queryset: QuerySet[models.BOJUser]):
        for obj in queryset:
            obj.schedule_update()

    @admin.action(description="Update selected BOJ user data right now. (via solved.ac API)")
    def update(self, request, queryset: QuerySet[models.BOJUser]):
        for obj in queryset:
            obj.update()


@admin.register(models.BOJUserSnapshot)
class BOJUserSnapshotModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUserSnapshot.field_name.USER,
        models.BOJUserSnapshot.field_name.LEVEL,
        models.BOJUserSnapshot.field_name.RATING,
        models.BOJUserSnapshot.field_name.CREATED_AT,
    ]
