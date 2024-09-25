from rest_framework import generics

from . import mixins
from . import permissions
from . import serializers


class SubmissionCreateAPIView(mixins.CrewActivityProblemUrlKwargMixin, generics.CreateAPIView):
    """문제에 대한 코드를 제출하는 API.\n\n."""
    permission_classes = [permissions.IsCrewMember]
    serializer_class = serializers.SubmissionDAOSerializer

    def perform_create(self, serializer: serializers.SubmissionDAOSerializer):
        serializer.save(problem=self.get_object(), user=self.request.user)


class SubmissionRetrieveDestroyAPIView(mixins.SubmissionUrlKwargMixin, generics.RetrieveDestroyAPIView):
    """제출된 코드를 조회(댓글 포함)/삭제하는 API.\n\n."""
    permission_classes = [permissions.IsCrewMember &
                          permissions.IsAuthorOrReadOnly]
    serializer_class = serializers.SubmissionDAOSerializer


class SubmissionCommentCreateAPIView(mixins.SubmissionUrlKwargMixin, generics.CreateAPIView):
    """제출된 코드에 대한 리뷰 댓글을 작성하는 API.\n\n."""
    permission_classes = [permissions.IsCrewMember]
    serializer_class = serializers.SubmissionCommentDAOSerializer

    def perform_create(self, serializer: serializers.SubmissionCommentDAOSerializer):
        serializer.save(submission=self.get_object(),
                        created_by=self.request.user)


class SubmissionCommentDestroyAPIView(mixins.SubmissionCommentUrlKwargMixin, generics.DestroyAPIView):
    """제출된 코드에 대한 댓글을 삭제하는 API.\n\n."""
    permission_classes = [permissions.IsCrewMember &
                          permissions.IsAuthorOrReadOnly]
    serializer_class = serializers.SubmissionCommentDAOSerializer
