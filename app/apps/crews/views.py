from rest_framework import generics

from apps.applications.serializers import CrewApplicationDTOSerializer
from apps.problems.serializers import ProblemStatisticDTOSerializer

from . import mixins
from . import permissions
from . import serializers
from .models import proxy


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록.\n\n."""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RecruitingCrewDTOSerializer

    def get_queryset(self):
        return proxy.Crew.objects.is_recruiting(self.request.user).as_recruiting_dto(self.request.user)


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewDTOSerializer

    def get_queryset(self):
        return proxy.Crew.objects.as_member(self.request.user).as_dto()


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API.\n\n."""
    queryset = proxy.Crew
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDAOSerializer


class CrewRetrieveUpdateAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveUpdateAPIView):
    """크루 대시보드 홈 API.\n\n."""
    permission_classes = [permissions.IsMember]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CrewDetailDTOSerializer
        return serializers.CrewDAOSerializer

    def get_object(self):
        if self.request.method == 'GET':
            return self.get_crew().as_detail_dto(self.request.user)
        return self.get_crew()


class CrewUpdateAPIView(mixins.CrewUrlKwargMixin, generics.UpdateAPIView):
    """크루 수정 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewDAOSerializer


class CrewApplicationListAPIView(mixins.CrewUrlKwargMixin, generics.ListAPIView):
    """크루 가입 신청 목록 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = CrewApplicationDTOSerializer

    def get_queryset(self):
        return self.get_crew().applications()


class CrewMemberListAPIView(mixins.CrewUrlKwargMixin, generics.ListAPIView):
    """크루 멤버 목록 API.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewMemberDTOSerializer

    def get_queryset(self):
        return self.get_crew().members()


class CrewStatisticsAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveAPIView):
    """크루 대시보드 문제 통계 API.\n\n.
    이 크루에 등록된 모든 문제에 대한 통계입니다."""
    permission_classes = [permissions.IsMember]
    serializer_class = ProblemStatisticDTOSerializer

    def get_object(self):
        return self.get_crew().statistics()
