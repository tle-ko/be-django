from django.contrib import admin

from apps.crews.submissions.models import *


admin.site.register([
    Submission,
    SubmissionComment,
])
