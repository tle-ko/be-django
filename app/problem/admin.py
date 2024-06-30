from django.contrib import admin

from .models import *


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProblemAnalysis)
class ProblemAnalysisAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
