from django.contrib import admin

from core.models import *


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
