from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from boj import models
from boj import services


@admin.register(models.BOJUser)
class BOJUserModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUser.field_name.USERNAME,
        models.BOJUser.field_name.LEVEL,
        models.BOJUser.field_name.RATING,
        models.BOJUser.field_name.UPDATED_AT,
    ]
    actions = [
        'fetch',
    ]

    @admin.action(description="Fetch data from solved.ac API of selected BOJ users.")
    def fetch(self, request: HttpRequest, queryset: QuerySet[models.BOJUser]):
        for obj in queryset:
            services.fetch(obj.username)


@admin.register(models.BOJUserSnapshot)
class BOJUserSnapshotModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUserSnapshot.field_name.USER,
        models.BOJUserSnapshot.field_name.LEVEL,
        models.BOJUserSnapshot.field_name.RATING,
        models.BOJUserSnapshot.field_name.CREATED_AT,
    ]
