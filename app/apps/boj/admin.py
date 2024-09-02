from django.contrib import admin
from django.db.models import QuerySet
from django.http.request import HttpRequest

from apps.boj.models import BOJUser
from apps.boj.models import BOJUserSnapshot
from apps.boj.services import schedule_update_boj_user_data
from apps.boj.services import update_boj_user


@admin.register(BOJUser)
class BOJUserModelAdmin(admin.ModelAdmin):
    list_display = [
        BOJUser.field_name.USERNAME,
        BOJUser.field_name.LEVEL,
        BOJUser.field_name.RATING,
        BOJUser.field_name.UPDATED_AT,
    ]
    actions = [
        'update',
        'schedule_update',
    ]

    @admin.action(description="Schedule update selected BOJ user data. (via solved.ac API)")
    def schedule_update(self, request: HttpRequest, queryset: QuerySet[BOJUser]):
        for obj in queryset:
            schedule_update_boj_user_data(obj.username)

    @admin.action(description="Update selected BOJ user data right now. (via solved.ac API)")
    def update(self, request: HttpRequest, queryset: QuerySet[BOJUser]):
        for obj in queryset:
            update_boj_user(obj)


@admin.register(BOJUserSnapshot)
class BOJUserSnapshotModelAdmin(admin.ModelAdmin):
    list_display = [
        BOJUserSnapshot.field_name.USER,
        BOJUserSnapshot.field_name.LEVEL,
        BOJUserSnapshot.field_name.RATING,
        BOJUserSnapshot.field_name.CREATED_AT,
    ]
