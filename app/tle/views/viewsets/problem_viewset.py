from rest_framework.viewsets import ModelViewSet

from tle.models import Problem
from tle.serializers import *
from tle.views.permissions import *


class ProblemViewSet(ModelViewSet):
    """문제 태그 목록 조회 + 생성 기능"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    # TODO: 내가 만든 문제만 수정할 수 있도록 변경

    def get_serializer_class(self):
        if self.action in ['create', 'list']:
            return ProblemMinimalSerializer
        return ProblemSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Problem.objects.all()
        # TODO: 내가 가입한 크루에서 풀어본 문제도 조회할 수 있도록 수정
        return Problem.objects.filter(created_by=user)
