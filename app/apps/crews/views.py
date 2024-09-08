from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from apps.activities.models import CrewActivityProblem
from apps.crews.models import Crew
from apps.crews.permissions import IsMember
from apps.crews.serializers import RecruitingCrewSerializer
from apps.crews.serializers import MyCrewSerializer
from apps.crews.serializers import CrewCreateSerializer
from apps.crews.serializers import CrewDashboardSerializer
from apps.problems.serializers import ProblemStatisticSerializer
from apps.problems.statistics import create_statistics


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록"""
    permission_classes = [AllowAny]
    serializer_class = RecruitingCrewSerializer

    def get_queryset(self):
        return Crew.objects.filter(
            not_as_member=self.request.user,
            is_recruiting=True,
        )


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루"""
    permission_classes = [IsAuthenticated & IsMember]
    serializer_class = MyCrewSerializer

    def get_queryset(self):
        return Crew.objects.filter(as_member=self.request.user).order_by(
            Crew.field_name.IS_ACTIVE,
            Crew.field_name.UPDATED_AT,
        ).reverse()


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API"""
    queryset = Crew
    permission_classes = [IsAuthenticated]
    serializer_class = CrewCreateSerializer


class CrewDashboardAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 API"""
    queryset = Crew
    permission_classes = [IsAuthenticated & IsMember]
    serializer_class = CrewDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'


class CrewStatisticsAPIView(generics.RetrieveAPIView):
    """크루 대시보드 문제 통계 API"""
    queryset = Crew
    permission_classes = [IsAuthenticated & IsMember]
    serializer_class = ProblemStatisticSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self):
        activity_problems = CrewActivityProblem.objects.crew(
            crew=super().get_object(),
        ).select_related(CrewActivityProblem.field_name.PROBLEM)
        return create_statistics([ap.problem for ap in activity_problems])
