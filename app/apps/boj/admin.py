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


@admin.register(proxy.BOJProblem)
class BOJProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.BOJProblem.field_name.PK,
        proxy.BOJProblem.field_name.TITLE,
        proxy.BOJProblem.field_name.LEVEL,
        proxy.BOJProblem.field_name.TAGS,
        proxy.BOJProblem.field_name.TIME_LIMIT,
        proxy.BOJProblem.field_name.TIME_LIMIT_DESCRIPTION,
        proxy.BOJProblem.field_name.MEMORY_LIMIT,
    ]
    search_fields = [
        proxy.BOJProblem.field_name.TITLE,
    ]
    ordering = [proxy.BOJProblem.field_name.PK]


@admin.register(proxy.BOJTag)
class BOJTagModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.BOJTag.field_name.KEY,
        proxy.BOJTag.field_name.NAME_KO,
        proxy.BOJTag.field_name.NAME_EN,
    ]
    search_fields = [
        proxy.BOJTag.field_name.KEY,
        proxy.BOJTag.field_name.NAME_KO,
        proxy.BOJTag.field_name.NAME_EN,
    ]
    ordering = [proxy.BOJTag.field_name.KEY]


@admin.register(proxy.BOJTagRelation)
class BOJTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.BOJTagRelation.field_name.PARENT,
        proxy.BOJTagRelation.field_name.CHILD,
    ]
    search_fields = [
        proxy.BOJTagRelation.field_name.PARENT,
        proxy.BOJTagRelation.field_name.CHILD,
    ]
    ordering = [proxy.BOJTagRelation.field_name.PARENT]
