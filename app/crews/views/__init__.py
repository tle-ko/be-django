from rest_framework import generics
from rest_framework import permissions

from crews import dto
from crews import models
from crews import serializers
from crews import services


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API"""

    queryset = models.Crew.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.RecruitingCrewSerializer


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록"""

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RecruitingCrewSerializer

    def get_queryset(self):
        # 본인이 속한 크루는 제외.
        queryset = services.crew.of_user_queryset(
            exclude_user=self.request.user,
        )
        return queryset.filter(**{
            models.Crew.field_name.IS_RECRUITING: True,
        })


class MyCrewAPIView(generics.ListAPIView):
    """나의 참여 크루"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MyCrewSerializer

    def get_queryset(self):
        queryset = services.crew.of_user_queryset(
            include_user=self.request.user,
        )
        # 활동 종료된 크루는 뒤로 가도록 정렬
        return queryset.order_by('-'+models.Crew.field_name.IS_ACTIVE)


class CrewDashboardAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDashboardSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return services.crew.of_user_queryset(
            include_user=self.request.user,
        )


class CrewStatisticsAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewStatisticsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return services.crew.of_user_queryset(
            include_user=self.request.user,
        )

    def get_object(self) -> dto.ProblemStatistic:
        return services.problem_statistics(crew=super().get_object())


class CrewActivityAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDashboardSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return services.crew.of_user_queryset(
            include_user=self.request.user,
        )
