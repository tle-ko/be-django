from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.crews.proxy import Crew
from apps.crews.permissions import IsCaptain as _IsCaptain

from . import models


class IsCaptain(_IsCaptain):
    def has_object_permission(self, request: Request, view, obj: models.CrewApplicationDAO):
        assert isinstance(obj, models.CrewApplicationDAO)
        return super().has_object_permission(request, view, obj.crew)


class IsAppliable(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: models.CrewApplicationDAO):
        assert isinstance(obj, models.CrewApplicationDAO)
        return Crew.is_appliable(obj.crew, request.user)
