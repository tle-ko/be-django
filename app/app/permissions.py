from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


__all__ = (
    'ReadOnly',
    'WriteOnly',
)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS,
        )


class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == 'POST',
        )
