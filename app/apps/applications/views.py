from rest_framework import generics
from rest_framework.response import Response

from . import models
from . import mixins
from . import permissions
from . import serializers
from .models import proxy


class CrewApplicationCreateAPIView(generics.CreateAPIView):
    """크루 가입 신청 API.\n\n."""
    queryset = proxy.CrewApplication
    permission_classes = [permissions.IsAppliable]
    serializer_class = serializers.CrewApplicationDAOSerializer

    def perform_create(self, serializer: serializers.CrewApplicationDAOSerializer):
        serializer.save(applicant=self.request.user)


class CrewApplicantionAcceptAPIView(mixins.CrewApplicationUrlKwargMixin, generics.GenericAPIView):
    """크루 가입 수락 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicantDTOSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accept(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CrewApplicantionRejectAPIView(mixins.CrewApplicationUrlKwargMixin, generics.GenericAPIView):
    """크루 가입 거부 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicantDTOSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reject(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
