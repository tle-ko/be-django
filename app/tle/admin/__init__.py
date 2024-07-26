from django.contrib import admin

from tle.models import *


admin.site.register([
    Submission,
    SubmissionComment,
])
