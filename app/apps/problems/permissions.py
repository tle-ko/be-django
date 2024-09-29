from django.http import HttpRequest
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsReadOnly

from . import models


class IsProblemCreator(IsAuthenticated):
    def has_object_permission(self, request: HttpRequest, view, obj):
        if isinstance(obj, models.ProblemDAO):
            return obj.created_by == request.user
        raise NotImplementedError('This permission is only for ProblemDAO instances')
