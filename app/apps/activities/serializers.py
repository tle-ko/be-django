from rest_framework import serializers

from apps.activities import models


PK = 'id'


class UserDTOSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    profile_image = serializers.CharField()


class UserSubmissionTableRowDTOSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    problem_title = serializers.CharField()
    problem_order = serializers.IntegerField()
    reviewers = UserDTOSerializer(many=True)
    created_at = serializers.DateTimeField()
    is_submitted = serializers.BooleanField()


class UserSubmissionTableDTOSerializer(serializers.Serializer):
    submissions = UserSubmissionTableRowDTOSerializer(many=True)
    submitted_by = UserDTOSerializer()


class CrewActivitySerializer(serializers.ModelSerializer):
    date_start_at = serializers.DateTimeField(source=models.CrewActivity.field_name.START_AT)
    date_end_at = serializers.DateTimeField(source=models.CrewActivity.field_name.END_AT)

    class Meta:
        model = models.CrewActivity
        fields = [
            models.CrewActivity.field_name.NAME,
            'date_start_at',
            'date_end_at',
        ]
        read_only_fields = ['__all__']
