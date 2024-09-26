from django.contrib import admin

from . import models


@admin.register(models.SubmissionDAO)
class SubmissionModelAdmin(admin.ModelAdmin):
    list_display = [
        models.SubmissionDAO.field_name.PROBLEM,
        models.SubmissionDAO.field_name.USER,
        models.SubmissionDAO.field_name.IS_CORRECT,
        models.SubmissionDAO.field_name.CREATED_AT,
    ]


@admin.register(models.SubmissionCommentDAO)
class SubmissionCommentModelAdmin(admin.ModelAdmin):
    list_display = [
        models.SubmissionCommentDAO.field_name.SUBMISSION,
        models.SubmissionCommentDAO.field_name.CONTENT,
        models.SubmissionCommentDAO.field_name.CREATED_BY,
        models.SubmissionCommentDAO.field_name.CREATED_AT,
    ]