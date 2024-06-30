from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)

from .models import Problem


__all__ = (
    'IsReadOnly',
    'IsCreateOnly',
    'IsAdminUser',
    'IsAuthenticated',
    'IsProblemCreator',
)


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS,
        )


class IsCreateOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == 'POST',
        )


class IsProblemCreator(IsAuthenticated):
    def has_object_permission(self, request, view, obj: Problem) -> bool:
        return super().has_object_permission(request, view, obj) and bool(
            obj.user == request.user
        )
