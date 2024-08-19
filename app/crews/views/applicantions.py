from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from crews import models
from crews import serializers
from crews import services


class CrewApplicantionCreateAPIView(generics.CreateAPIView):
    queryset = models.Crew
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewApplicationSerializer
    lookup_field = 'id'

    def perform_create(self, serializer: serializers.CrewApplicationSerializer):
        instance = serializer.save(**{
            models.CrewApplicant.field_name.CREW: self.get_object(),
            models.CrewApplicant.field_name.USER: self.request.user,
        })
        services.crew_applicant.notify_captain(instance)


class CrewApplicantionAcceptAPIView(generics.GenericAPIView):
    queryset = models.CrewApplicant.objects
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance: models.CrewApplicant = self.get_object()
        services.crew_applicant.accept(instance, self.request.user)
        services.crew_applicant.notify_accepted(instance)
        return Response(status=status.HTTP_200_OK)


class CrewApplicantionRejectAPIView(generics.GenericAPIView):
    queryset = models.CrewApplicant.objects
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance: models.CrewApplicant = self.get_object()
        services.crew_applicant.reject(instance, self.request.user)
        services.crew_applicant.notify_rejected(instance)
        return Response(status=status.HTTP_200_OK)
