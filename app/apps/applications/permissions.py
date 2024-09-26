from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from apps.crews.proxy import Crew
from apps.crews.permissions import IsCaptain as _IsCaptain

from . import models


class IsCaptain(_IsCaptain):
    def has_object_permission(self, request: Request, view, obj):
        if isinstance(obj, models.CrewApplicationDAO):
            obj = obj.crew
        return super().has_object_permission(request, view, obj)


class IsAppliable(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj):
        if isinstance(obj, models.CrewApplicationDAO):
            return Crew.is_appliable(obj.crew, request.user)
        raise ValueError(f'Unexpected object type: {obj.__class__.__name__}')
