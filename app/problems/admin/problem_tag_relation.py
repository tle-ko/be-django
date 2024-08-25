from django.contrib import admin

from problems import models


@admin.register(models.ProblemTagRelation)
class ProblemTagRelationModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemTagRelation.field_name.PARENT,
        models.ProblemTagRelation.field_name.CHILD,
    ]
    search_fields = [
        models.ProblemTagRelation.field_name.PARENT,
        models.ProblemTagRelation.field_name.CHILD,
    ]
    ordering = [models.ProblemTagRelation.field_name.PARENT]
