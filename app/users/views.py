from django.contrib.auth import logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework import throttling
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from users import models
from users.serializers import IsEmailUsableSerializer
from users.serializers import IsUsernameUsableSerializer
from users.serializers import SignInSerializer
from users.serializers import SignUpSerializer
from users import serializers
from users import services


class EmailCheckAPIView(generics.GenericAPIView):
    """이메일이 사용가능한지 검사 API"""

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = IsEmailUsableSerializer

    @swagger_auto_schema(query_serializer=IsEmailUsableSerializer)
    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UsernameCheckAPIView(generics.GenericAPIView):
    """이메일이 사용가능한지 검사 API"""
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = IsUsernameUsableSerializer

    @swagger_auto_schema(query_serializer=IsUsernameUsableSerializer)
    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class SignInAPIView(generics.GenericAPIView):
    """사용자 로그인 API"""
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_login(serializer)
        return Response(serializer.data)

    def perform_login(self, serializer: SignInSerializer):
        serializer.save()


class SignUpAPIView(generics.CreateAPIView):
    """사용자 등록(회원가입) API"""
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class SignOutAPIView(generics.GenericAPIView):
    """사용자 로그아웃 API"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailVerifyThrottle(throttling.AnonRateThrottle):
    THROTTLE_RATES = '1/min'


class EmailVerifyAPIView(generics.GenericAPIView):
    """이메일 인증 코드 전송 API"""
    authentication_classes = []
    throttle_classes = []
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.EmailSerializer
        if self.request.method == 'POST':
            return serializers.EmailCodeSerializer
        raise ValueError

    @swagger_auto_schema(
        operation_description="이메일을 입력하면, 입력된 이메일 주소로 인증 코드를 발송합니다. 해당 코드를 동일한 주소의 POST 요청으로 전달하면 회원가입시 사용할 수 있는 인증 토큰을 반환합니다.",
        query_serializer=serializers.EmailSerializer,
        responses={
            status.HTTP_201_CREATED: '이메일 인증 코드 생성 성공 및 발신 완료',
            status.HTTP_400_BAD_REQUEST: '잘못된 이메일 혹은 이미 동일한 이메일로 가입된 계정이 존재.',
        },
    )
    def get(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        services.send_verification_code(email)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: '이메일 인증 성공. 새로운 이메일 인증 토큰을 발급받는다. 이 때 받은 토큰은 회원 가입시 이메일 소유 증명을 위해 제출해야한다.',
            status.HTTP_400_BAD_REQUEST: '잘못된 이메일 혹은 올바르지 않은 인증번호.',
        },
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        return Response(
            data={
                'email': email,
                'token': services.get_verification_token(email, code),
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """현재 로그인한 사용자 정보를 조회/수정하는 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserUpdateSerializer

    def get_object(self) -> models.User:
        return self.request.user
