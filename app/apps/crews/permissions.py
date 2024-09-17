from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.crews.models import Crew
from apps.crews.models import CrewMember


class IsMember(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: Crew):
        assert isinstance(obj, Crew)
        return CrewMember.objects.filter(crew=obj, user=request.user).exists()


class IsCaptain(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: Crew) -> bool:
        assert isinstance(obj, Crew)
        return CrewMember.objects.filter(crew=obj, user=request.user, is_captain=True).exists()
