from django.contrib import admin

from apps.submissions.models import *


admin.site.register([
    Submission,
    SubmissionComment,
])
