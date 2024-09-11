from rest_framework import generics
from rest_framework.response import Response

from apps.activities import models
from apps.activities import permissions
from apps.activities import serializers
from apps.activities import services
from apps.crews.models import CrewMember


class CrewDashboardActivityAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 별 API"""
    queryset = models.CrewActivity
    permission_classes = []  # TODO
    serializer_class = ...  # TODO
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'


class ActivitySubmissionsAPIView(generics.ListAPIView):
    """멤버별로 각 문제마다 제출한 것들을 조회.

    ."""
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.UserSubmissionTableDTOSerializer
    queryset = models.CrewActivity
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    def list(self, request, *args, **kwargs):
        activity: models.CrewActivity = self.get_object()
        serializer = serializers.UserSubmissionTableDTOSerializer([
            services.get_user_submission_table(activity=activity, user=member.user)
            for member in CrewMember.objects.filter(crew=activity.crew)
        ], many=True)
        return Response(serializer.data)
