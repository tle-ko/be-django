from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from crews import models
from crews import permissions
from crews import serializers


class CrewActivityRetrieveAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 API"""
    queryset = models.CrewActivity
    permission_classes = [IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.CrewActivityDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'
