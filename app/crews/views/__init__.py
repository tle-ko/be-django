from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

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
        queryset = services.crew_of_user_queryset(
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
        queryset = services.crew_of_user_queryset(
            include_user=self.request.user,
        )
        # 활동 종료된 크루는 뒤로 가도록 정렬
        return queryset.order_by('-'+models.Crew.field_name.IS_ACTIVE)


class CrewDashboardAPIView(generics.RetrieveAPIView):
    """가입한 크루 목록 조회 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MyCrewDashboardSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return services.crew_of_user_queryset(
            include_user=self.request.user,
        )
