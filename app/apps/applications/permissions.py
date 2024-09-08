from rest_framework.request import Request

from apps.applications.models import CrewApplication
from apps.crews.permissions import IsCaptain as _IsCaptain


class IsCaptain(_IsCaptain):
    def has_object_permission(self, request: Request, view, obj: CrewApplication):
        assert isinstance(obj, CrewApplication)
        return super().has_object_permission(request, view, obj.crew)
