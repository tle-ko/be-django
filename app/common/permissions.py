from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsReadOnly(BasePermission):
    def has_permission(self, request: HttpRequest, view):
        return request.method in SAFE_METHODS
