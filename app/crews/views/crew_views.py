from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crews import dto
from crews import models
from crews import permissions
from crews import serializers
from crews import services


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API"""
    queryset = models.Crew.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CrewCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = serializers.MyCrewSerializer(instance=instance)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록"""
    permission_classes = [AllowAny]
    serializer_class = serializers.RecruitingCrewSerializer

    def get_queryset(self):
        return services.CrewService.query_recruiting(self.request.user)


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루"""
    permission_classes = [IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.MyCrewSerializer

    def get_queryset(self):
        queryset = services.CrewService.query_as_member(self.request.user)
        # 활동 종료된 크루는 뒤로 가도록 정렬
        return queryset.order_by('-'+models.Crew.field_name.IS_ACTIVE)


class CrewDashboardAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 API"""
    queryset = models.Crew
    permission_classes = [IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.CrewDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_queryset(self):
        return services.CrewService.query_as_member(self.request.user)


class CrewStatisticsAPIView(generics.RetrieveAPIView):
    queryset = models.Crew
    permission_classes = [IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.CrewStatisticsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self) -> dto.ProblemStatistic:
        crew = super().get_object()
        service = services.CrewService(crew)
        return service.statistics()


class CrewApplicationsListAPIView(generics.ListAPIView):
    queryset = models.Crew
    permission_classes = [IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationAboutApplicantSerializer
    lookup_url_kwarg = 'crew_id'

    def get_queryset(self):
        crew_id = self.kwargs[self.lookup_url_kwarg]
        try:
            crew = models.Crew.objects.get(pk=crew_id)
        except models.Crew.DoesNotExist:
            raise exceptions.NotFound
        return models.CrewApplication.objects.filter(**{
            models.CrewApplication.field_name.CREW: crew,
        })
