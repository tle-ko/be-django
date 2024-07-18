from http import HTTPStatus

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from tle.models import User
from tle.serializers import *
from tle.views.permissions import *


class AuthViewSet(GenericViewSet):
    """사용자 계정과 관련된 API

    current: 현재 로그인한 사용자 정보
    signup: 사용자 등록(회원가입)
    signin: 사용자 로그인
    signout: 사용자 로그아웃
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    # Overrides

    def get_serializer_class(self):
        if self.action == 'sign_in':
            return UserSignInSerializer
        else:
            return UserSerializer

    # Helpers

    def get_validated_serializer(self, request: Request) -> Serializer:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def authenticate(self, request: Request) -> User:
        serializer = self.get_validated_serializer(request)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        return user

    # Actions

    def sign_up(self, request: Request):
        serializer = self.get_validated_serializer(request)
        serializer.save()
        return Response(serializer.data)

    def sign_in(self, request: Request):
        serializer = self.get_validated_serializer(request)
        serializer.instance = self.authenticate(request)
        login(request, serializer.instance)
        return Response(serializer.data)

    def sign_out(self, request: Request):
        logout(request)
        return Response(status=HTTPStatus.OK)

    # TODO: 이메일 인증
    # TODO: 비밀번호 찾기
