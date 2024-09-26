from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status

from apps.applications.serializers import CrewApplicationDTOSerializer
from apps.problems.serializers import ProblemStatisticDTOSerializer

from . import mixins
from . import permissions
from . import serializers
from . import proxy


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

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CrewRetrieveUpdateAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveUpdateAPIView):
    """크루 상세 조회/수정 API.\n\n대시보드에 사용된다.."""
    permission_classes = [permissions.IsCaptain |
                          permissions.IsMemberAndReadOnly]
    serializer_class = serializers.CrewDAOSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)



class CrewStatisticsAPIView(mixins.CrewUrlKwargMixin, generics.RetrieveAPIView):
    """크루 대시보드 문제 통계 API.\n\n.
    이 크루에 등록된 모든 문제에 대한 통계입니다."""
    permission_classes = [permissions.IsMember]
    serializer_class = ProblemStatisticDTOSerializer

    def get_object(self):
        return super().get_object().statistics()
