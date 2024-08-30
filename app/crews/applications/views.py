from django.http.request import HttpRequest
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from crews.applications.models import CrewApplication
from crews.applications.permissions import IsCaptain
from crews.applications.services import review
from crews.applications import serializers
from crews.models import Crew
from crews import servicesa


class CrewApplicationForCrewListAPIView(generics.ListAPIView):
    """[크루/관리/크루 멤버 관리] 크루 가입 신청 현황 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CrewApplicationSerializer
    lookup_url_kwarg = 'crew_id'

    def get_queryset(self):
        return CrewApplication.objects.filter(crew=self.get_crew())

    def get_crew(self) -> Crew:
        crew_id = self.kwargs[self.lookup_url_kwarg]
        try:
            return Crew.objects.filter(as_captain=self.request.user).get(pk=crew_id)
        except Crew.DoesNotExist:
            raise ValidationError("크루가 존재하지 않거나, 권한이 없습니다.")


class CrewApplicationForUserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CrewApplicationSerializer

    def get_queryset(self):
        return CrewApplication.objects.filter(applicant=self.request.user)


class CrewApplicantionCreateAPIView(generics.CreateAPIView):
    """크루 가입 신청 API"""
    queryset = CrewApplication
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CrewApplicationCreateSerializer
    lookup_url_kwarg = 'crew_id'

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = serializers.CrewApplicationSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: serializers.CrewApplicationCreateSerializer):
        crew_id = self.kwargs[self.lookup_url_kwarg]
        try:
            crew = Crew.objects.get(pk=crew_id)
        except Crew.DoesNotExist:
            raise NotFound("크루가 존재하지 않습니다.")

        message = serializer.validated_data['message']
        service = servicesa.get_crew_service(crew=self.get_object())
        serializer.instance = service.apply(self.request.user, message)


class CrewApplicantionAcceptAPIView(generics.UpdateAPIView):
    """크루 가입 수락 API"""
    queryset = CrewApplication
    permission_classes = [IsAuthenticated & IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_serializer(self, instance, *args, **kwargs) -> serializers.CrewApplicationSerializer:
        return serializers.CrewApplicationSerializer(instance)

    def perform_update(self, serializer: serializers.CrewApplicationSerializer):
        review(serializer.instance, self.request.user, accept=True)


class CrewApplicantionRejectAPIView(generics.UpdateAPIView):
    """크루 가입 거부 API"""
    queryset = CrewApplication
    permission_classes = [IsAuthenticated & IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_serializer(self, instance, *args, **kwargs) -> serializers.CrewApplicationSerializer:
        return serializers.CrewApplicationSerializer(instance)

    def perform_update(self, serializer: serializers.CrewApplicationSerializer):
        review(serializer.instance, self.request.user, accept=False)
