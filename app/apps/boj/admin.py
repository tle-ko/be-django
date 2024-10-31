from django.contrib import admin
from django.db.models import QuerySet

from . import models
from . import services


@admin.register(models.BOJUserDAO)
class BOJUserModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUserDAO.field_name.USERNAME,
        models.BOJUserDAO.field_name.LEVEL,
        models.BOJUserDAO.field_name.RATING,
        models.BOJUserDAO.field_name.UPDATED_AT,
    ]
    actions = [
        'update',
        'schedule_update',
    ]

    @admin.action(description="Schedule update selected BOJ user data. (via solved.ac API)")
    def schedule_update(self, request, queryset: QuerySet[models.BOJUserDAO]):
        for obj in queryset:
            services.schedule_update_boj_user_data(obj.username)

    @admin.action(description="Update selected BOJ user data right now. (via solved.ac API)")
    def update(self, request, queryset: QuerySet[models.BOJUserDAO]):
        for obj in queryset:
            services.update_boj_user_data(obj.username)


@admin.register(models.BOJUserSnapshotDAO)
class BOJUserSnapshotModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJUserSnapshotDAO.field_name.USER,
        models.BOJUserSnapshotDAO.field_name.LEVEL,
        models.BOJUserSnapshotDAO.field_name.RATING,
        models.BOJUserSnapshotDAO.field_name.CREATED_AT,
    ]


@admin.register(models.BOJProblemDAO)
class BOJProblemModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJProblemDAO.field_name.PK,
        models.BOJProblemDAO.field_name.TITLE,
        models.BOJProblemDAO.field_name.LEVEL,
        models.BOJProblemDAO.field_name.TAGS,
        models.BOJProblemDAO.field_name.TIME_LIMIT,
        models.BOJProblemDAO.field_name.TIME_LIMIT_DESCRIPTION,
        models.BOJProblemDAO.field_name.MEMORY_LIMIT,
    ]
    search_fields = [
        models.BOJProblemDAO.field_name.TITLE,
    ]
    ordering = [models.BOJProblemDAO.field_name.PK]


@admin.register(models.BOJTagDAO)
class BOJTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJTagDAO.field_name.KEY,
        models.BOJTagDAO.field_name.NAME_KO,
        models.BOJTagDAO.field_name.NAME_EN,
    ]
    search_fields = [
        models.BOJTagDAO.field_name.KEY,
        models.BOJTagDAO.field_name.NAME_KO,
        models.BOJTagDAO.field_name.NAME_EN,
    ]
    ordering = [models.BOJTagDAO.field_name.KEY]


@admin.register(models.BOJTagRelationDAO)
class BOJTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        models.BOJTagRelationDAO.field_name.PARENT,
        models.BOJTagRelationDAO.field_name.CHILD,
    ]
    search_fields = [
        models.BOJTagRelationDAO.field_name.PARENT,
        models.BOJTagRelationDAO.field_name.CHILD,
    ]
    ordering = [models.BOJTagRelationDAO.field_name.PARENT]
