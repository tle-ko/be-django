from django.contrib import admin

from . import proxy


@admin.register(proxy.Submission)
class SubmissionModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.Submission.field_name.PROBLEM,
        proxy.Submission.field_name.USER,
        proxy.Submission.field_name.IS_CORRECT,
        proxy.Submission.field_name.CREATED_AT,
    ]


@admin.register(proxy.SubmissionComment)
class SubmissionCommentModelAdmin(admin.ModelAdmin):
    list_display = [
        proxy.SubmissionComment.field_name.SUBMISSION,
        proxy.SubmissionComment.field_name.CONTENT,
        proxy.SubmissionComment.field_name.CREATED_BY,
        proxy.SubmissionComment.field_name.CREATED_AT,
    ]