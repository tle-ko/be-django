from rest_framework import generics

from crews.activities import models
from crews import permissions
from crews import serializersaaa


class CrewDashboardActivityAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 별 API"""
    queryset = models.CrewActivity
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = serializersaaa.CrewActivityDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'
