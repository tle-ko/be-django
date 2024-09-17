from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import permissions
from rest_framework.request import Request

from common.pagination import LargeResultsSetPagination

from . import models
from . import serializers


class ProblemCreateAPIView(generics.CreateAPIView):
    """문제 생성 API.\n\n."""

    queryset = models.Problem
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDAOSerializer


class ProblemDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """문제 상세 조회, 수정, 삭제 API.\n\n."""

    queryset = models.Problem
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDAOSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'


class ProblemSearchListAPIView(generics.ListAPIView):
    """문제 검색 API.\n\n
    제목에 q로 주어진 문자열을 포함하는 문제들을 나열한다.
    q를 입력하지 않았을 경우, 모든 문제를 나열한다."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ProblemDTOSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return models.Problem.objects.created_by(self.request.user).search(self.get_query_string())

    def get_query_string(self) -> str:
        self.request: Request
        data = self.request.query_params
        serializer = serializers.ProblemSearchQueryParamSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['q']

    @swagger_auto_schema(query_serializer=serializers.ProblemSearchQueryParamSerializer)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
