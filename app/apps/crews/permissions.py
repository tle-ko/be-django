from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

from . import proxy
from . import models


class IsMember(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj: models.CrewDAO):
        assert isinstance(obj, models.CrewDAO)
        return proxy.CrewMember.objects.filter(crew=obj, user=request.user).exists()


class IsMemberAndReadOnly(IsMember):
    def has_permission(self, request: HttpRequest, view) -> bool:
        return super().has_permission(request, view) and (request.method in SAFE_METHODS)


class IsCaptain(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj: models.CrewDAO) -> bool:
        assert isinstance(obj, models.CrewDAO)
        return proxy.CrewMember.objects.filter(crew=obj, user=request.user, is_captain=True).exists()
