from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.crews.models import CrewDAO
from apps.crews.proxy import CrewMember


class IsMember(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: CrewDAO):
        assert isinstance(obj, CrewDAO)
        return CrewMember.objects.filter(crew=obj, user=request.user).exists()


class IsCaptain(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: CrewDAO) -> bool:
        assert isinstance(obj, CrewDAO)
        return CrewMember.objects.filter(crew=obj, user=request.user, is_captain=True).exists()
