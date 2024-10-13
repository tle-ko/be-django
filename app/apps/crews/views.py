import typing

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from . import converters
from . import models
from . import permissions
from . import serializers


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록.\n\n."""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RecruitingCrewDTOSerializer

    def get_queryset(self):
        queryset = models.CrewDAO.objects \
            .filter(**{models.CrewDAO.field_name.IS_RECRUITING: True}) \
            .exclude(**{models.CrewDAO.field_name.PK+'__in': self.crew_ids_as_member(self.request.user)}) \
            .order_by('-'+models.CrewDAO.field_name.IS_ACTIVE)
        return converters.CrewConverter().queryset_to_dto(queryset)

    def crew_ids_as_member(self, user: models.User) -> typing.List[int]:
        if user.is_anonymous:
            return []
        return models.CrewMemberDAO.objects \
            .filter(**{models.CrewMemberDAO.field_name.USER: user}) \
            .values_list(models.CrewMemberDAO.field_name.CREW, flat=True)


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewDTOSerializer

    def get_queryset(self):
        queryset = models.CrewDAO.objects \
            .filter(**{models.CrewDAO.field_name.PK+'__in': self.crew_ids_as_member(self.request.user)})
        return converters.CrewConverter().queryset_to_dto(queryset)

    def crew_ids_as_member(self, user: models.User) -> typing.List[int]:
        if user.is_anonymous:
            return []
        return models.CrewMemberDAO.objects \
            .filter(**{models.CrewMemberDAO.field_name.USER: user}) \
            .values_list(models.CrewMemberDAO.field_name.CREW, flat=True)


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API.\n\n."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDAOSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CrewRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """크루 상세 조회/수정 API.\n\n대시보드에 사용된다.."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsCaptain |
                          (permissions.IsMember & permissions.IsReadOnly)]
    serializer_class = serializers.CrewDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CrewStatisticsAPIView(generics.RetrieveAPIView):
    """크루 대시보드 문제 통계 API.\n\n.
    이 크루에 등록된 모든 문제에 대한 통계입니다."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewStatisticsDTOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self):
        return converters.CrewStatisticsConverter().instance_to_dto(super().get_object())


class CrewApplicationListAPIView(generics.ListAPIView):
    """크루 가입 신청 목록 API.\n\n."""
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDTOSerializer
    lookup_url_kwarg = 'crew_id'

    def get_crew(self) -> models.CrewDAO:
        return generics.get_object_or_404(models.CrewDAO, **{models.CrewDAO.field_name.PK: self.kwargs[self.lookup_url_kwarg]})

    def get_queryset(self):
        queryset = self.get_crew().get_applications()
        return converters.CrewApplicationConverter(self.request.user).queryset_to_dto(queryset)


class CrewApplicationCreateAPIView(generics.CreateAPIView):
    """크루 가입 신청 API.\n\n."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsAppliable]
    serializer_class = serializers.CrewApplicationDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def perform_create(self, serializer: serializers.CrewApplicationDAOSerializer):
        return serializer.save(**{models.CrewApplicationDAO.field_name.CREW: self.get_object()})


class CrewApplicantionAcceptAPIView(generics.GenericAPIView):
    """크루 가입 수락 API.\n\n."""
    queryset = models.CrewApplicationDAO
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_object(self) -> models.CrewApplicationDAO:
        return super().get_object()

    @swagger_auto_schema(
        request_body=serializers.EmptySerializer,
        responses={200: serializer_class.dto_serializer_class}
    )
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reject(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CrewApplicantionRejectAPIView(generics.GenericAPIView):
    """크루 가입 거부 API.\n\n."""
    queryset = models.CrewApplicationDAO
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_object(self) -> models.CrewApplicationDAO:
        return super().get_object()

    @swagger_auto_schema(
        request_body=serializers.EmptySerializer,
        responses={200: serializer_class.dto_serializer_class}
    )
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reject(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CrewActivityCreateAPIView(generics.CreateAPIView):
    """크루 활동 생성 API.\n\n."""
    queryset = models.CrewDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain]
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewActivityDAOSerializer):
        serializer.save(**{
            models.CrewActivityDAO.field_name.CREW: self.get_object(),
        })


class CrewActivityRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """크루 활동 상세 조회 API.\n\n."""
    queryset = models.CrewActivityDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain |
                          (permissions.IsMember & permissions.IsReadOnly)]
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CrewActivityProblemRetrieveAPIView(generics.RetrieveAPIView):
    """크루 활동 문제 상세 조회 API.\n\n."""
    queryset = models.CrewProblemDAO
    serializer_class = serializers.CrewActivityProblemDAOSerializer
    permission_classes = [permissions.IsMember & permissions.IsReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
