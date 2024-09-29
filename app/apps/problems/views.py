from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import generics
from rest_framework import status

from common.pagination import LargeResultsSetPagination

from . import converters
from . import models
from . import permissions
from . import serializers


class ProblemCreateAPIView(generics.CreateAPIView):
    """문제 생성 API.\n\n."""

    queryset = models.ProblemDAO
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDAOSerializer

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: serializer_class.serializer_class})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProblemDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """문제 상세 조회, 수정, 삭제 API.\n\n."""

    queryset = models.ProblemDAO
    permission_classes = [permissions.IsProblemCreator | permissions.IsReadOnly]
    serializer_class = serializers.ProblemDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_ref_id'

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.serializer_class})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializer_class.serializer_class})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProblemSearchListAPIView(generics.ListAPIView):
    """문제 검색 API.\n\n
    제목에 q로 주어진 문자열을 포함하는 문제들을 나열한다.
    q를 입력하지 않았을 경우, 모든 문제를 나열한다."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDTOSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [models.ProblemDAO.field_name.TITLE]

    def get_queryset(self):
        return models.ProblemDAO.objects.filter(**{
            models.ProblemDAO.field_name.CREATED_BY: self.request.user,
        })

    def get_serializer(self, queryset, *args, **kwargs):
        queryset = converters.ProblemConverter().queryset_to_dto(queryset)
        return super().get_serializer(queryset, *args, **kwargs)