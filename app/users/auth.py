from django.contrib import auth
from django.http import HttpRequest
from rest_framework import exceptions

from . import models
from . import serializers


def login(request: HttpRequest, serializer: serializers.UserDAOSignInSerializer) -> None:
    instance: models.User
    instance = auth.authenticate(request, **serializer.validated_data)
    if instance is None:
        raise exceptions.AuthenticationFailed('이메일 혹은 비밀번호가 올바르지 않습니다.')
    auth.login(request, instance)
    instance.rotate_token()
    instance.save()
    serializer.instance = instance


def logout(request: HttpRequest) -> None:
    auth.logout(request)
