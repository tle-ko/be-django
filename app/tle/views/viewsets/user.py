from http import HTTPStatus

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tle.models import User
from tle.serializers import (
    UserSerializer,
    UserSignUpSerializer,
    UserSignInSerializer,
)
from tle.views.permissions import *


class UserViewSet(GenericViewSet):
    """사용자 계정과 관련된 API

    current: 현재 로그인한 사용자 정보
    signup: 사용자 등록(회원가입)
    signin: 사용자 로그인
    signout: 사용자 로그아웃
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    SERIALIZERS = {
        'sign_up': UserSignUpSerializer,
        'sign_in': UserSignInSerializer,
    }

    def get_serializer(self, *args, **kwargs):
        if self.action in self.__class__.SERIALIZERS:
            return self.__class__.SERIALIZERS[self.action](*args, **kwargs)
        return UserSerializer(*args, **kwargs)

    def current(self, request: Request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    def sign_up(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.instance = User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data)

    def sign_in(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email, password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        login(request, user)
        serializer.instance = user
        return Response(serializer.data)

    def sign_out(self, request: Request):
        logout(request)
        return Response(status=HTTPStatus.OK)

    # TODO: 이메일 인증

    # TODO: 비밀번호 찾기
