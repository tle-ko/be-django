from django.contrib import admin

from .models import proxy


admin.site.register([
    proxy.Submission,
    proxy.SubmissionComment,
])
