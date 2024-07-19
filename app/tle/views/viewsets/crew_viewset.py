from rest_framework.viewsets import ModelViewSet

from tle.models import Crew
from tle.serializers import *
from tle.views.permissions import *


class CrewViewSet(ModelViewSet):
    """문제 태그 목록 조회 + 생성 기능"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        if self.action in 'list_recruiting':
            return Crew.objects.filter(is_recruiting=True)
        return Crew.objects.all()

    def get_serializer_class(self):
        if self.action in 'list_recruiting':
            return CrewRecruitingSerializer

    def list_recruiting(self, request):
        return super().list(request)
