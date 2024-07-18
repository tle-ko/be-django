from django.contrib import admin

from tle.admin.user import UserModelAdmin
from tle.admin.problem import ProblemModelAdmin
from tle.admin.problem_tag import ProblemTagModelAdmin
from tle.admin.submission_language import SubmissionLanguageModelAdmin
from tle.models import *


__all__ = (
    'UserModelAdmin',
    'ProblemModelAdmin',
    'ProblemTagModelAdmin',
    'SubmissionLanguageModelAdmin',
)

admin.site.register([
    Crew,
    CrewActivity,
    CrewActivityProblem,
    CrewApplicant,
    CrewMember,
    ProblemAnalysis,
    Submission,
    SubmissionComment,
])
