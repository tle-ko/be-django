from django.contrib import admin

from problem.models import *


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(ProblemAnalysis)
class ProblemAnalysisAdmin(admin.ModelAdmin):
    pass
