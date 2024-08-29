from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from crews.models import Crew
from crews.models import CrewMember


class IsMember(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Crew):
        assert isinstance(obj, Crew)
        return CrewMember.objects.filter(crew=obj, user=request.user).exists()


class IsCaptain(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Crew) -> bool:
        assert isinstance(obj, Crew)
        return CrewMember.objects.filter(crew=obj, user=request.user, is_captain=True).exists()
