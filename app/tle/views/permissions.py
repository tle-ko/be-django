from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS,
)


__all__ = (
    'AllowAny',
    'IsAuthenticated',
    'IsAdminUser',

    'IsReadOnly',
)


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS,
        )
