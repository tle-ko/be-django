from django.http.request import HttpRequest
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from crews import models
from crews import permissions
from crews import serializers
from crews import services
from problems.dto import ProblemStatisticDTO
from problems.serializers import ProblemStatisticSerializer


# Crew List API Views

class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록"""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RecruitingCrewSerializer

    def get_queryset(self):
        service = services.get_user_crew_service(self.request.user)
        return service.query_crews_recruiting()


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루"""
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.MyCrewSerializer

    def get_queryset(self):
        service = services.get_user_crew_service(self.request.user)
        return service.query_crews_joined()


# Crew API Views

class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API"""
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = serializers.MyCrewSerializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CrewDashboardAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 API"""
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.CrewDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'


class CrewStatisticsAPIView(generics.RetrieveAPIView):
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = ProblemStatisticSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self) -> ProblemStatisticDTO:
        instance = super().get_object()
        service = services.get_crew_service(instance)
        return service.statistics()


# Crew Activity API Views

class CrewDashboardActivityAPIView(generics.RetrieveAPIView):
    """크루 대시보드 홈 - 회차 별 API"""
    queryset = models.CrewActivity
    permission_classes = [permissions.IsAuthenticated & permissions.IsMember]
    serializer_class = serializers.CrewActivityDashboardSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'


# Crew Application API Views

class CrewApplicationListAPIView(generics.RetrieveAPIView):
    """[크루/관리/크루 멤버 관리] 크루 가입 신청 현황 API"""
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationAboutApplicantSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        service = services.get_crew_service(instance)
        queryset = service.query_applications()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CrewApplicantionCreateAPIView(generics.CreateAPIView):
    """크루 가입 신청 API"""
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated & permissions.IsJoinable]
    serializer_class = serializers.CrewApplicationCreateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = serializers.CrewApplicationSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: serializers.CrewApplicationCreateSerializer):
        message = serializer.validated_data['message']
        service = services.get_crew_service(crew=self.get_object())
        serializer.instance = service.apply(self.request.user, message)


class CrewApplicantionAcceptAPIView(generics.GenericAPIView):
    """크루 가입 수락 API"""
    queryset = models.CrewApplication
    permission_classes = [permissions.IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def put(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        service = services.get_crew_application_service(instance)
        service.accept(reviewed_by=request.user)
        serializer = serializers.CrewApplicationSerializer(instance)
        return Response(serializer.data)


class CrewApplicantionRejectAPIView(generics.GenericAPIView):
    """크루 가입 거부 API"""
    queryset = models.CrewApplication
    permission_classes = [permissions.IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def put(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        service = services.get_crew_application_service(instance)
        service.reject(reviewed_by=request.user)
        serializer = serializers.CrewApplicationSerializer(instance)
        return Response(serializer.data)
