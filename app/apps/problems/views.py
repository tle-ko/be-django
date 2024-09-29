from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.request import Request

from common.pagination import LargeResultsSetPagination

from . import models
from . import permissions
from . import serializers


class ProblemCreateAPIView(generics.CreateAPIView):
    """문제 생성 API.\n\n."""

    queryset = models.ProblemDAO
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDAOSerializer

    @swagger_auto_schema(request_body=serializer_class.serializer_class)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: serializers.ProblemDAOSerializer):
        return serializer.save(created_by=self.request.user)


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

    @swagger_auto_schema(query_serializer=serializers.ProblemSearchQueryParamSerializer)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return models.ProblemDAO.objects.filter(**{
            models.ProblemDAO.field_name.TITLE + '__icontains': self.get_query_params(self.request),
            models.ProblemDAO.field_name.CREATED_BY: self.request.user,
        })

    def get_query_params(self, request: Request) -> str:
        serializer = serializers.ProblemSearchQueryParamSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['q']
