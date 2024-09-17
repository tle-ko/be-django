from rest_framework import serializers

from users.serializers import UserDTOSerializer


class SubmissionDTOSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField(source='pk')
    is_correct = serializers.BooleanField()
    submitted_at = serializers.DateTimeField()
    submitted_by = UserDTOSerializer()
