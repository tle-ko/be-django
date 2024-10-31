from rest_framework import serializers

from users.serializers import UserDTOSerializer

from . import proxy


class SubmissionDTOSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()
    submitted_at = serializers.DateTimeField()
    submitted_by = UserDTOSerializer()
    reviewers = UserDTOSerializer(many=True)


class SubmissionCommentDTOSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    content = serializers.CharField()
    line_number_start = serializers.IntegerField()
    line_number_end = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    created_by = UserDTOSerializer()


class SubmissionDetailDTOSerializer(SubmissionDTOSerializer):
    code = serializers.CharField()
    comments = SubmissionCommentDTOSerializer(many=True)


class SubmissionDAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = proxy.Submission
        fields = [
            proxy.Submission.field_name.CODE,
            proxy.Submission.field_name.USER,
            proxy.Submission.field_name.LANGUAGE,
            proxy.Submission.field_name.IS_CORRECT,
        ]
        extra_kwargs = {
            proxy.Submission.field_name.USER: {'read_only': True},
        }

    @property
    def data(self):
        self.instance: proxy.Submission
        return SubmissionDetailDTOSerializer(self.instance.as_detail_dto()).data


class SubmissionCommentDAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = proxy.SubmissionComment
        fields = [
            proxy.SubmissionComment.field_name.CONTENT,
            proxy.SubmissionComment.field_name.LINE_NUMBER_START,
            proxy.SubmissionComment.field_name.LINE_NUMBER_END,
        ]

    @property
    def data(self):
        self.instance: proxy.SubmissionComment
        return SubmissionCommentDTOSerializer(self.instance.as_dto()).data
