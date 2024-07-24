from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from tle.models import Crew
from tle.serializers import *
from tle.views.permissions import *


class CrewPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet):
        if view.action == 'list_recruiting':
            # 모든 사용자에게 공개
            return True
        if view.action == 'list_my':
            return request.user.is_authenticated


class CrewViewSet(ModelViewSet):
    """문제 태그 목록 조회 + 생성 기능"""
    lookup_field = 'id'
    permission_classes = [CrewPermission]

    def get_queryset(self):
        if self.action in 'list_recruiting':
            return Crew.objects.filter(is_recruiting=True)
        if self.action in 'list_my':
            return Crew.of_user(self.request.user).order_by('-'+Crew.field_name.IS_ACTIVE)
        return Crew.objects.all()

    def get_serializer_class(self):
        if self.action in 'list_recruiting':
            return CrewRecruitingSerializer
        if self.action in 'list_my':
            return CrewJoinedSerializer

    def list_recruiting(self, request):
        # TODO: 검색 옵션 (사용 언어 / 백준 티어) 제공
        return super().list(request)

    def list_my(self, request):
        return super().list(request)
