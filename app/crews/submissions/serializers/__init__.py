from rest_framework import serializers

from crews.submissions.models import Submission


class SubmissionSerializer(serializers.ModelField):
    class Meta:
        model = Submission
        fields = [
            'id',
            Submission.field_name.USER,
            Submission.field_name.CODE,
            Submission.field_name.LANGUAGE,
            Submission.field_name.IS_CORRECT,
            Submission.field_name.IS_HELP_NEEDED,
            Submission.field_name.CREATED_AT,
        ]
