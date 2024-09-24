from django.contrib import admin

from . import proxy


admin.site.register([
    proxy.Submission,
    proxy.SubmissionComment,
])
