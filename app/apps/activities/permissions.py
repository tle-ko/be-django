from rest_framework.permissions import IsAuthenticated

from apps.activities.models import CrewActivity
from apps.crews.permissions import IsMember as _IsMember


class IsMember(_IsMember):
    def has_object_permission(self, request, view, obj: CrewActivity):
        return super().has_object_permission(request, view, obj.crew)