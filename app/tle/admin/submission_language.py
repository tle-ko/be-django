from django.contrib import admin

from tle.models import SubmissionLanguage


@admin.register(SubmissionLanguage)
class SubmissionLanguageModelAdmin(admin.ModelAdmin):
    list_display = ['key', 'name', 'extension']
    search_fields = ['key', 'name', 'extension']
    ordering = ['key']
