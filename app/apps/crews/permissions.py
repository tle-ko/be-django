from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsReadOnly

from . import models


__all__ = [
    'AllowAny',
    'IsAuthenticated',
    'IsReadOnly',
    'IsMember',
    'IsCaptain',
    'IsAppliable',
]


class IsMember(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj):
        return models.CrewMemberDAO.objects.filter(**{
            models.CrewMemberDAO.field_name.CREW: _get_crew(obj),
            models.CrewMemberDAO.field_name.USER: request.user,
        }).exists()


class IsCaptain(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return models.CrewMemberDAO.objects.filter(**{
            models.CrewMemberDAO.field_name.CREW: _get_crew(obj),
            models.CrewMemberDAO.field_name.USER: request.user,
            models.CrewMemberDAO.field_name.IS_CAPTAIN: True,
        }).exists()


class IsAppliable(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return _get_crew(obj).is_appliable(request.user)


def _get_crew(obj):
    if isinstance(obj, models.CrewDAO):
        return obj
    if isinstance(obj, models.CrewActivityDAO):
        return obj.crew
    if isinstance(obj, models.CrewProblemDAO):
        return obj.crew
    raise NotImplementedError
