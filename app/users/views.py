from typing import Callable

from django.contrib.auth import authenticate, login, logout
from rest_framework import (
    mixins,
    permissions,
    status,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from users.models import User, UserManager
from users.serializers import UserDetailSerializer, UserSignInSerializer


class SignUp(mixins.CreateModelMixin,
             GenericAPIView):
    """사용자 등록(회원가입) API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer: Serializer):
        user_manager: UserManager = User.objects
        user = user_manager.create_user(**serializer.validated_data)
        serializer.instance = user


class SignIn(mixins.RetrieveModelMixin,
             GenericAPIView):
    """사용자 로그인 API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSignInSerializer

    get_serializer: Callable[..., Serializer]

    def get_object(self) -> User:
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # 사용자 인증을 위한 email과 password를 추출
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # 사용자 인증
        user = authenticate(self.request, username=email, password=password)
        # 사용자 인증 실패 시 예외 발생
        if user is None:
            raise AuthenticationFailed('Invalid email or password')
        # 사용자 인증 성공 시 (세션) 로그인
        login(self.request, user)
        return user

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SignOut(GenericAPIView):
    """사용자 로그아웃 API"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUser(mixins.RetrieveModelMixin,
                  GenericAPIView):
    """현재 로그인한 사용자 정보 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self) -> User:
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
