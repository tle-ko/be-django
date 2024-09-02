from django.contrib import admin

from crews.submissions.models import *


admin.site.register([
    Submission,
    SubmissionComment,
])
