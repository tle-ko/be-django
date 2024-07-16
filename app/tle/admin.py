from django.contrib import admin

from tle.models import *


@admin.register(
    User,

    Crew,
    CrewActivity,
    CrewActivityProblem,
    CrewApplicant,
    CrewMember,

    Problem,
    ProblemAnalysis,
    ProblemTag,

    Submission,
    SubmissionComment,
    SubmissionLanguage,
)
class SuperAdmin(admin.ModelAdmin):
    pass
