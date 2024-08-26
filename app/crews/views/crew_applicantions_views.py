from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from crews import models
from crews import permissions
from crews import serializers
from crews import services


class CrewApplicantionCreateAPIView(generics.CreateAPIView):
    queryset = models.Crew
    permission_classes = [IsAuthenticated & permissions.IsJoinable]
    serializer_class = serializers.CrewApplicationCreateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def create(self, request: Request, *args, **kwargs):
        # input serializer
        serializer = self.get_serializer(data=request.data)
        instance = services.CrewApplicantionService.create(
            crew=self.get_object(),
            user=request.user,
            message=serializer.validated_data['message'],
        )
        # output serializer
        serializer = serializers.CrewApplicationAboutApplicantSerializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CrewApplicantionAcceptAPIView(generics.GenericAPIView):
    queryset = models.CrewApplication
    permission_classes = [IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def put(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        service = services.CrewApplicantionService(instance)
        service.accept(reviewed_by=request.user)
        serializer = serializers.CrewApplicationAboutApplicantSerializer(instance)
        return Response(serializer.data)


class CrewApplicantionRejectAPIView(generics.GenericAPIView):
    queryset = models.CrewApplication
    permission_classes = [IsAuthenticated & permissions.IsCaptain]
    serializer_class = serializers.NoInputSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def put(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        service = services.CrewApplicantionService(instance)
        service.reject(reviewed_by=request.user)
        serializer = serializers.CrewApplicationAboutApplicantSerializer(instance)
        return Response(serializer.data)
