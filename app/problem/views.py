from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import *


__all__ = (
    'TagViewSet',
    'LanguageViewSet',
    'ProblemViewSet',
    'AnalysisViewSet',
)


class TagViewSet(viewsets.ModelViewSet):
    """문제 태그 목록 조회 + 생성 기능"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class LanguageViewSet(viewsets.ModelViewSet):
    """프로그래밍 언어 목록 조회 + 생성 기능"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class ProblemViewSet(viewsets.ModelViewSet):
    """문제 목록 조회 + 생성 기능

    - 관리자는 전체 문제 목록을 조회할 수 있습니다.
    - 관리자가 아닌 일반 사용자는 자신이 만든 문제만 조회할 수 있습니다.
    """
    serializer_class = ProblemSerializer
    permission_classes = [IsAdminUser | IsProblemCreator | IsReadOnly | (IsAuthenticated & IsCreateOnly)]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Problem.objects.all()
        return Problem.objects.filter(user=self.request.user)

    def my_list(self, request: Request):
        """내가 만든 문제 목록 조회"""
        queryset = Problem.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AnalysisViewSet(viewsets.ModelViewSet):
    """문제 태그 목록 조회 + 생성 기능"""
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [IsAdminUser | IsReadOnly]
    lookup_field = 'problem__id'
    lookup_url_kwarg = 'pk'
