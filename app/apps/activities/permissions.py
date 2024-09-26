from apps.crews.permissions import IsCaptain as _IsCaptain
from apps.crews.permissions import IsMemberAndReadOnly as _IsMemberAndReadOnly


from . import models


class IsCaptain(_IsCaptain):
    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, models.CrewActivityDAO):
            obj = obj.crew
        if isinstance(obj, models.CrewActivityProblemDAO):
            obj = obj.crew
        return super().has_object_permission(request, view, obj)


class IsMemberAndReadOnly(_IsMemberAndReadOnly):
    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, models.CrewActivityDAO):
            obj = obj.crew
        if isinstance(obj, models.CrewActivityProblemDAO):
            obj = obj.crew
        return super().has_object_permission(request, view, obj)
