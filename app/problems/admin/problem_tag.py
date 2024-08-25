from django.contrib import admin

from problems import models


@admin.register(models.ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = [
        models.ProblemTag.field_name.KEY,
        models.ProblemTag.field_name.NAME_KO,
        models.ProblemTag.field_name.NAME_EN,
    ]
    search_fields = [
        models.ProblemTag.field_name.KEY,
        models.ProblemTag.field_name.NAME_KO,
        models.ProblemTag.field_name.NAME_EN,
    ]
    ordering = [models.ProblemTag.field_name.KEY]
