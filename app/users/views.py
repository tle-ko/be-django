from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from . import auth
from . import models
from . import serializers


class UsabilityAPIView(generics.RetrieveAPIView):
    """이메일/사용자명이 사용 가능한지 조회하는 API.

    이메일 혹은 사용자명 중 하나만 입력해도 동작하지만,
    둘 다 입력하지 않을 경우 400 BAD_REQUEST를 반환한다.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UsabilitySerializer

    @swagger_auto_schema(query_serializer=serializers.UsabilitySerializerForQueryParameter)
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
    permission_classes = [permissions.AllowAny]
    queryset = models.UserEmailVerification
    serializer_class = serializers.EmailVerificationSerializer

    def get_object(self):
        email = self.request.data['email']
        return models.UserEmailVerification.objects.get_or_create_by_email(email=email)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SignInAPIView(generics.GenericAPIView):
    """사용자 로그인 API.\n\n."""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserDAOSignInSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.UserDAOSignInSerializer.dto_serializer_class})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth.login(request, serializer)
        return Response(serializer.data)


class SignUpAPIView(generics.CreateAPIView):
    """사용자 등록(회원가입) API.\n\n."""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserDAOSignUpSerializer


class SignOutAPIView(generics.GenericAPIView):
    """사용자 로그아웃 API.\n\n."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserManageAPIView(generics.RetrieveUpdateAPIView):
    """현재 로그인한 사용자 정보를 조회/수정하는 API.\n\n."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserDAOSerializer

    def get_object(self) -> models.User:
        return self.request.user

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.UserDAOSerializer.dto_serializer_class})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.UserDAOSerializer.dto_serializer_class})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: serializers.UserDAOSerializer.dto_serializer_class})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
