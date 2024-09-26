from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from . import mixins
from . import permissions
from . import proxy
from . import serializers


class CrewApplicationListAPIView(mixins.CrewUrlKwargMixin, generics.ListAPIView):
    """크루 가입 신청 목록 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDTOSerializer

    def get_queryset(self):
        return super().get_object().applications()


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
    serializer_class = serializers.serializers.Serializer

    @swagger_auto_schema(responses={200: serializers.CrewApplicationDTOSerializer})
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accept(self.request.user)
        return Response(serializers.CrewApplicationDTOSerializer(instance.as_dto()).data)


class CrewApplicantionRejectAPIView(mixins.CrewApplicationUrlKwargMixin, generics.GenericAPIView):
    """크루 가입 거부 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.serializers.Serializer

    @swagger_auto_schema(responses={200: serializers.CrewApplicationDTOSerializer})
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reject(self.request.user)
        return Response(serializers.CrewApplicationDTOSerializer(instance.as_dto()).data)
