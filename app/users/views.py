from typing import Callable

from rest_framework import (
    mixins,
    permissions,
    status,
)
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from users.models import User
from users.serializers import *
from users.services import *


__all__ = (
    'SignUp',
    'SignIn',
    'SignOut',
    'CurrentUser',
    'EmailVerification',
)


class SignUp(mixins.CreateModelMixin,
             GenericAPIView):
    """사용자 등록(회원가입) API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserDetailSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer: Serializer):
        token = serializer.validated_data.pop('verification_token')
        VerificationService.validate_verification_token(token)
        user = AuthenticationService.sign_up(**serializer.validated_data)
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
        return AuthenticationService.sign_in(
            request=self.request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SignOut(GenericAPIView):
    """사용자 로그아웃 API"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        AuthenticationService.sign_out(request)
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


class EmailVerification(GenericAPIView):
    """이메일 인증 요청 API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = UserEmailSerializer

    get_serializer: Callable[..., Serializer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserEmailSerializer
        if self.request.method == 'POST':
            return UserEmailVerificationCodeSerializer

    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if VerificationService.is_verified(email):
            raise ValidationError('Email is already verified.')
        code = VerificationService.get_verification_code(email)
        VerificationService.send_verification_code(email, code)
        return Response(status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        token = VerificationService.get_verification_token(email, code)
        serializer.validated_data['token'] = token
        return Response(serializer.data, status=status.HTTP_200_OK)
