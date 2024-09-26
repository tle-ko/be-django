from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView

from apps.activities.mixins import CrewActivityProblemUrlKwargMixin

from . import proxy


class SubmissionUrlKwargMixin:
    queryset = proxy.Submission
    lookup_field = 'id'
    lookup_url_kwarg = 'submission_id'

    def get_submission(self: GenericAPIView) -> proxy.Submission:
        return get_object_or_404(proxy.Submission, pk=self.kwargs[self.lookup_field])


class SubmissionCommentUrlKwargMixin:
    queryset = proxy.SubmissionComment
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_submission_comment(self: GenericAPIView) -> proxy.SubmissionComment:
        return get_object_or_404(proxy.SubmissionComment, pk=self.kwargs[self.lookup_field])
