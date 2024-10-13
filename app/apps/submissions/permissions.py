import typing

from django.http import HttpRequest
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from apps.crews.permissions import IsMember

from . import models


class IsCrewMember(IsMember):
    def has_object_permission(self, request: HttpRequest, view: GenericAPIView, obj):
        if isinstance(obj, models.SubmissionDAO):
            obj: models.SubmissionDAO
            return super().has_object_permission(request, view, obj.problem.crew)
        if isinstance(obj, models.SubmissionCommentDAO):
            obj: models.SubmissionCommentDAO
            return super().has_object_permission(request, view, obj.submission.problem.crew)
        if isinstance(obj, models.CrewProblemDAO):
            obj: models.CrewProblemDAO
            return super().has_object_permission(request, view, obj.crew)
        raise ValueError(f'Unsupported object type: {type(obj)}')


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request: HttpRequest, view: GenericAPIView, obj):
        if request.method in SAFE_METHODS:
            return True
        if isinstance(obj, models.SubmissionDAO):
            obj: models.SubmissionDAO
            return obj.user == request.user
        if isinstance(obj, models.SubmissionCommentDAO):
            obj: models.SubmissionCommentDAO
            return obj.created_by == request.user
        raise ValueError(f'Unsupported object type: {type(obj)}')
