from rest_framework import generics

from apps.problems.serializers import ProblemStatisticDTOSerializer

from . import mixins
from . import models
from . import permissions
from . import serializers


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록.\n\n."""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CrewDTOSerializer

    def get_queryset(self):
        return models.Crew.objects.is_recruiting(self.request.user)


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewDTOSerializer

    def get_queryset(self):
        return models.Crew.objects.as_member(self.request.user)


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API.\n\n."""
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewCreateSerializer


class CrewDashboardAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveAPIView):
    """크루 대시보드 홈 API.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewDashboardDTOSerializer

    def get_object(self):
        return self.get_crew().dashboard(self.request.user)


class CrewStatisticsAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveAPIView):
    """크루 대시보드 문제 통계 API.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = ProblemStatisticDTOSerializer

    def get_object(self):
        return self.get_crew().statistics()
