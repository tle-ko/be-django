from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from tle.models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = [
        *BaseUserAdmin.fieldsets,
        (None, {'fields': [
            'profile_image',
            'boj_username',
            'boj_tier',
            'boj_tier_updated_at',
        ]}),
    ]


admin.site.register([
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
])
