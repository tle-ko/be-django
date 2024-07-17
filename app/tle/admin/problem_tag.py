from django.contrib import admin

from tle.models import ProblemTag


@admin.register(ProblemTag)
class ProblemTagModelAdmin(admin.ModelAdmin):
    list_display = ['parent', 'key', 'name_ko', 'name_en']
    search_fields = ['parent', 'key', 'name_ko', 'name_en']
    ordering = ['key']
