from rest_framework import generics
from rest_framework import mixins
from rest_framework import status

from common import swagger

from . import converters
from . import models
from . import permissions
from . import serializers


class RecruitingCrewListAPIView(generics.ListAPIView):
    """크루 목록.\n\n."""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RecruitingCrewDTOSerializer

    def get_queryset(self):
        queryset = models.CrewDAO.objects.not_as_member(self.request.user) \
            .filter(**{models.CrewDAO.field_name.IS_RECRUITING: True}) \
            .order_by('-'+models.CrewDAO.field_name.IS_ACTIVE)
        return converters.RecruitingCrewConverter(self.request.user).queryset_to_dto(queryset)

    @swagger.auto_schema(tags=[swagger.Tags.CREW])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyCrewListAPIView(generics.ListAPIView):
    """나의 참여 크루.\n\n."""
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewDTOSerializer

    def get_queryset(self):
        queryset = models.CrewDAO.objects.as_member(self.request.user)
        return converters.CrewConverter().queryset_to_dto(queryset)

    @swagger.auto_schema(tags=[swagger.Tags.CREW])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrewCreateAPIView(generics.CreateAPIView):
    """크루 생성 API.\n\n."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CrewDAOSerializer

    @swagger.auto_schema(tags=[swagger.Tags.CREW], responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
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

    @swagger.auto_schema(tags=[swagger.Tags.CREW], responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger.auto_schema(tags=[swagger.Tags.CREW], responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger.auto_schema(tags=[swagger.Tags.CREW], responses={status.HTTP_200_OK: serializers.CrewDetailDTOSerializer})
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

    @swagger.auto_schema(tags=[swagger.Tags.CREW])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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

    @swagger.auto_schema(tags=[swagger.Tags.CREW, swagger.Tags.CREW_APPLICATION])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrewApplicationCreateAPIView(generics.CreateAPIView):
    """크루 가입 신청 API.\n\n."""
    queryset = models.CrewDAO
    permission_classes = [permissions.IsAppliable]
    serializer_class = serializers.CrewApplicationDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW, swagger.Tags.CREW_APPLICATION], responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewApplicationDAOSerializer):
        return serializer.save(**{models.CrewApplicationDAO.field_name.CREW: self.get_object()})


class CrewApplicantionAcceptAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """크루 가입 수락 API.\n\n."""
    queryset = models.CrewApplicationDAO
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDTOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def _get_object(self) -> models.CrewApplicationDAO:
        return super().get_object()

    def get_object(self) -> models.CrewApplicationDAO:
        instance = self._get_object()
        instance.accept(self.request.user)
        return converters.CrewApplicantConverter().instance_to_dto(instance)

    @swagger.auto_schema(tags=[swagger.Tags.CREW_APPLICATION], request_body=serializers.EmptySerializer, responses={status.HTTP_200_OK: serializer_class})
    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CrewApplicantionRejectAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """크루 가입 거부 API.\n\n."""
    queryset = models.CrewApplicationDAO
    permission_classes = [permissions.IsCaptain]
    serializer_class = serializers.CrewApplicationDTOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def _get_object(self) -> models.CrewApplicationDAO:
        return super().get_object()

    def get_object(self) -> models.CrewApplicationDAO:
        instance = self._get_object()
        instance.reject(self.request.user)
        return converters.CrewApplicantConverter().instance_to_dto(instance)

    @swagger.auto_schema(tags=[swagger.Tags.CREW_APPLICATION], request_body=serializers.EmptySerializer, responses={status.HTTP_200_OK: serializer_class})
    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CrewActivityCreateAPIView(generics.CreateAPIView):
    """크루 활동 생성 API.\n\n."""
    queryset = models.CrewDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain]
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW, swagger.Tags.CREW_ACTIVITY], responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewActivityDAOSerializer):
        return serializer.save(**{models.CrewActivityDAO.field_name.CREW: self.get_object()})


class CrewActivityRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """크루 활동 상세 조회 API.\n\n."""
    queryset = models.CrewActivityDAO
    serializer_class = serializers.CrewActivityDAOSerializer
    permission_classes = [permissions.IsCaptain |
                          (permissions.IsMember & permissions.IsReadOnly)]
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_ACTIVITY], responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger.auto_schema(tags=[swagger.Tags.CREW_ACTIVITY], responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger.auto_schema(tags=[swagger.Tags.CREW_ACTIVITY], responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CrewActivityProblemRetrieveAPIView(generics.RetrieveAPIView):
    """크루 활동 문제 상세 조회 API.\n\n."""
    queryset = models.CrewProblemDAO
    serializer_class = serializers.CrewActivityProblemDAOSerializer
    permission_classes = [permissions.IsMember & permissions.IsReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_ACTIVITY, swagger.Tags.CREW_PROBLEM], responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrewSubmissionCreateAPIView(generics.CreateAPIView):
    """문제에 대한 코드를 제출하는 API.\n\n."""
    queryset = models.CrewProblemDAO
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewSubmissionDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_PROBLEM, swagger.Tags.CREW_SUBMISSION], responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewSubmissionDAOSerializer):
        return serializer.save(**{models.CrewSubmissionDAO.field_name.PROBLEM: self.get_object()})


class CrewSubmissionRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """제출된 코드를 조회(댓글 포함)/삭제하는 API.\n\n."""
    queryset = models.CrewSubmissionDAO
    permission_classes = [permissions.IsMember &
                          (permissions.IsAuthor | permissions.IsReadOnly)]
    serializer_class = serializers.CrewSubmissionDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'submission_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_SUBMISSION], responses={status.HTTP_200_OK: serializer_class.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger.auto_schema(tags=[swagger.Tags.CREW_SUBMISSION])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CrewSubmissionCommentCreateAPIView(generics.CreateAPIView):
    """제출된 코드에 대한 리뷰 댓글을 작성하는 API.\n\n."""
    queryset = models.CrewSubmissionDAO
    permission_classes = [permissions.IsMember]
    serializer_class = serializers.CrewSubmissionCommentDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'submission_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_SUBMISSION], responses={status.HTTP_201_CREATED: serializer_class.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.CrewSubmissionCommentDAOSerializer):
        return serializer.save(**{models.CrewSubmissionCommentDAO.field_name.SUBMISSION: self.get_object()})


class CrewSubmissionCommentDestroyAPIView(generics.DestroyAPIView):
    """제출된 코드에 대한 댓글을 삭제하는 API.\n\n."""
    queryset = models.CrewSubmissionCommentDAO
    permission_classes = [permissions.IsMember &
                          (permissions.IsAuthor | permissions.IsReadOnly)]
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    @swagger.auto_schema(tags=[swagger.Tags.CREW_SUBMISSION])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
