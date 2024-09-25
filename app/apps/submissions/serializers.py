from rest_framework import serializers
from .proxy import Submission, SubmissionComment
from users.dto import UserDTO
from users.models import User
from users.serializers import UserSerializer
from users.serializers import UserDTOSerializer
from .dto import SubmissionDTO


class SubmissionSerializer(serializers.ModelSerializer):
    """
    문제에 대한 코드를 제출하는 Serializer
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Submission
        fields = ['problem', 'user', 'code', 'language', 'is_correct', 'is_help_needed']
        ref_name = 'SubmissionSerializer'

class SubmissionCommentSerializer(serializers.ModelSerializer):
    """
    제출된 코드에 대한 리뷰 댓글 Serializer
    """
    created_by = UserSerializer()

    class Meta:
        model = SubmissionComment
        fields = ['id', 'line_number_start', 'line_number_end', 'content', 'created_by', 'created_at']
        ref_name = 'SubmissionCommentSerializer'

class SubmissionDetailSerializer(serializers.ModelSerializer):
    comments = SubmissionCommentSerializer(many=True)  # Submission과 관련된 댓글들
    user = UserDTOSerializer(source='get_user_dto')  

    class Meta:
        model = Submission  # Django의 Submission 모델을 사용
        fields = ['id', 'problem', 'code', 'language', 'is_correct', 'is_help_needed', 'created_at', 'user', 'comments']
        ref_name = 'SubmissionDetailSerializer' 

class SubmissionDTOSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()
    is_correct = serializers.BooleanField()
    submitted_at = serializers.DateTimeField()
    submitted_by = UserDTOSerializer()

    class Meta:
        ref_name = 'SubmissionDTOSerializer'

class SubmissionCommentSerializer(serializers.ModelSerializer):
    """
    제출된 코드에 대한 리뷰 댓글 Serializer
    """
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = SubmissionComment
        fields = ['id', 'line_number_start', 'line_number_end', 'content', 'created_by', 'created_at']

    def create(self, validated_data):
        # 댓글 생성 시 created_by와 submission을 저장합니다.
        return SubmissionComment.objects.create(
            created_by=validated_data.pop('created_by'),
            submission=validated_data.pop('submission'),
            **validated_data
        )
