from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *

from app.permissions import ReadOnly

from .models import *
from .serializers import *


class _PageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsProblemCreator(BasePermission):
    def has_object_permission(self, request, view, obj: Problem) -> bool:
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.user == request.user
        )


class ProblemAPIView:
    class ListCreate(ListCreateAPIView):
        """전체 문제 목록 조회 + 생성 기능

        - 관리자는 전체 문제 목록을 조회할 수 있습니다.
        - 관리자가 아닌 일반 사용자는 자신이 만든 문제만 조회할 수 있습니다.
        """
        serializer_class = ProblemSerializer
        pagination_class = _PageNumberPagination
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            if self.request.user.is_staff:
                return Problem.objects.all()
            # TODO: 공개된 문제도 보여주도록 기능 추가
            return Problem.objects.filter(user=self.request.user)


    class MyList(ListAPIView):
        """내가 만든 문제 목록 조회"""
        serializer_class = ProblemSerializer
        pagination_class = _PageNumberPagination
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            return Problem.objects.filter(user=self.request.user)


    class RetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Problem.objects.all()
        serializer_class = ProblemSerializer
        permission_classes = [IsAdminUser | IsProblemCreator]
        lookup_url_kwarg = 'id'


class ProblemAnalysisAPIView:
    class Retrieve(RetrieveAPIView):
        queryset = ProblemAnalysis.objects.all()
        permission_classes = [IsAdminUser | (IsProblemCreator & ReadOnly)]
        serializer_class = ProblemAnalysisSerializer
        lookup_url_kwarg = 'id'
        lookup_field = 'problem__id'
