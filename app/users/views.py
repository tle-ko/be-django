from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User
from users.models import UserEmailVerification
from users.serializers import EmailVerificationSerializer
from users.serializers import UsabilitySerializerForQueryParameter
from users.serializers import UsabilitySerializer
from users.serializers import UserUpdateSerializer
from users.serializers import SignInSerializer
from users.serializers import SignUpSerializer


class UsabilityAPIView(generics.RetrieveAPIView):
    """이메일/사용자명이 사용 가능한지 조회하는 API.

    이메일 혹은 사용자명 중 하나만 입력해도 동작하지만,
    둘 다 입력하지 않을 경우 400 BAD_REQUEST를 반환한다.
    """

    permission_classes = [AllowAny]
    serializer_class = UsabilitySerializer

    @swagger_auto_schema(query_serializer=UsabilitySerializerForQueryParameter)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(request.query_params)
        return Response(serializer.data)


class EmailVerificationAPIView(generics.mixins.UpdateModelMixin,
                               generics.GenericAPIView):
    """이메일을 인증하기 위한 API.

    이메일만 전달하면 새로운 코드를 발급 후 이메일로 전송해준다.
    코드를 함께 전달하면 새로운 인증 토큰을 발급하여 반환한다.
    """
    authentication_classes = []
    throttle_classes = []
    permission_classes = [AllowAny]
    queryset = UserEmailVerification
    serializer_class = EmailVerificationSerializer

    def get_object(self):
        email = self.request.data['email']
        return UserEmailVerification.objects.get_or_create_by_email(email=email)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SignInAPIView(generics.GenericAPIView):
    """사용자 로그인 API.

    .
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_login(serializer)
        return Response(serializer.data)

    def perform_login(self, serializer: SignInSerializer):
        user: Optional[User]
        if (user := authenticate(request=self.request, **serializer.validated_data)) is None:
            raise AuthenticationFailed(f'Invalid email or password')
        login(self.request, user)
        user.rotate_token()  # TODO: 이 작업을 로그인 백엔드에서 수행하도록 변경
        serializer.instance = user


class SignUpAPIView(generics.CreateAPIView):
    """사용자 등록(회원가입) API.

    .
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class SignOutAPIView(generics.GenericAPIView):
    """사용자 로그아웃 API.

    .
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserManageAPIView(generics.RetrieveUpdateAPIView):
    """현재 로그인한 사용자 정보를 조회/수정하는 API.

    .
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self) -> User:
        return self.request.user
