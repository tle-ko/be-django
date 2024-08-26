from typing import Union

from rest_framework import exceptions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from crews import models
from crews import services


class IsJoinable(BasePermission):
    def has_object_permission(self, request: Request, view, crew: models.Crew):
        assert isinstance(crew, models.Crew)
        service = services.CrewService(crew)
        try:
            service.validate_applicant(request.user, raises_exception=True)
        except exceptions.ValidationError as exception:
            detail = f"크루에 가입할 수 없습니다. ({exception.args[0]})"
            raise exceptions.PermissionDenied(detail)
        return True


class IsMember(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Union[models.Crew, models.CrewActivity]):
        if isinstance(obj, models.Crew):
            crew = obj
        elif isinstance(obj, models.CrewActivity):
            crew = obj.crew
        else:
            raise ValueError('백엔드의 실책으로 보이는 오류')
        service = services.CrewService(crew)
        if not service.is_member(request.user):
            raise exceptions.PermissionDenied('크루 멤버가 아닙니다.')
        return True


class IsCaptain(BasePermission):
    def has_object_permission(self, request: Request, view, application: models.CrewApplication) -> bool:
        assert isinstance(application, models.CrewApplication)
        service = services.CrewService(application.crew)
        return service.is_captain(request.user)
