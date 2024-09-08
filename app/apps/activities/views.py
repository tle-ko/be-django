from rest_framework import generics

from apps.activities import models


class CrewDashboardActivityAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 별 API"""
    queryset = models.CrewActivity
    permission_classes = [] # TODO
    serializer_class = ... # TODO
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'
