from typing import Callable

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, permissions, status, throttling
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from users import serializers, services
from users.models import User


__all__ = (
    'SignUpAPIView',
    'SignInAPIView',
    'SignOutAPIView',
    'CurrentUserAPIView',
    'EmailVerification',
)


class SignInAPIView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    """사용자 로그인 API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SignInSerializer
    get_serializer: Callable[..., Serializer]

    def get_object(self) -> User:
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return services.sign_in(
            request=self.request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: '로그인 성공',
        status.HTTP_401_UNAUTHORIZED: '로그인 실패',
    })
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.UserSerializer(instance)
        return Response(serializer.data)


class SignUpAPIView(generics.CreateAPIView):
    """사용자 등록(회원가입) API"""

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.SignUpSerializer

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: '회원가입 성공',
        status.HTTP_400_BAD_REQUEST: '잘못 입력한 값이 존재',
    })
    def perform_create(self, serializer: Serializer):
        token = serializer.validated_data.pop('verification_token')
        services.verify_token(token)
        user = services.sign_up(**serializer.validated_data)
        serializer.instance = user


class SignOutAPIView(APIView):
    """사용자 로그아웃 API"""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={
        status.HTTP_204_NO_CONTENT: '로그아웃 성공',
    })
    def get(self, request, *args, **kwargs):
        services.sign_out(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserAPIView(generics.RetrieveAPIView):
    """현재 로그인한 사용자 정보 API"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get_object(self) -> User:
        return self.request.user


class EmailCheckAPIView(generics.GenericAPIView):
    """이메일이 사용가능한지 검사 API"""
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.EmailSerializer
    get_serializer: Callable[..., Serializer]

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: '검사를 수행했을 경우, 사용가능 여부를 Boolean으로 반환함.',
        status.HTTP_400_BAD_REQUEST: '잘못된 이메일 형식.',
    })
    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        return Response(data={
            "email": email,
            "is_usable": services.is_usable(email),
        }, status=status.HTTP_200_OK)


class EmailVerifyAPIView(generics.GenericAPIView):
    """이메일 인증 코드 전송 API"""

    permission_classes = [permissions.AllowAny]
    get_serializer: Callable[..., Serializer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.EmailSerializer
        if self.request.method == 'POST':
            return serializers.EmailCodeSerializer
        raise ValueError

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: '이메일 인증 코드 생성 성공 및 발신 완료',
        status.HTTP_400_BAD_REQUEST: '잘못된 이메일 혹은 이미 동일한 이메일로 가입된 계정이 존재.',
    })
    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        services.send_verification_code(email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: '이메일 인증 성공. 새로운 이메일 인증 토큰을 발급받는다. 이 때 받은 토큰은 회원 가입시 이메일 소유 증명을 위해 제출해야한다.',
        status.HTTP_400_BAD_REQUEST: '잘못된 이메일 혹은 올바르지 않은 인증번호.',
    })
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        return Response(data={
            'email': email,
            'token': services.get_verification_token(email, code),
        }, status=status.HTTP_200_OK)
