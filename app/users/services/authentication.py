"""인증과 관련된 서비스들입니다.

사용자 로그인, 회원가입, 로그아웃 로직을 담고 있습니다.
"""
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, UserEmailVerification, UserManager


def sign_up(email: str, username: str, password: str, **extra_fields) -> User:
    """회원가입

    이메일 인증 토큰이 필요합니다.
    인증에 실패할 경우 ValidationError를 발생시킵니다."""
    user_manager: UserManager = User.objects
    verification_token = extra_fields.pop('verification_token', None)
    # 이메일 주소 인증
    if not UserEmailVerification.objects.filter(**{
        UserEmailVerification.field_name.EMAIL: email,
        UserEmailVerification.field_name.VERIFICATION_TOKEN: verification_token
    }).exists():
        raise ValidationError('Email is not verified.')
    return user_manager.create_user(email, username, password, **extra_fields)

def sign_in(request: Request, email: str, password: str) -> User:
    """로그인

    사용자 인증에 실패할 경우 AuthenticationFailed를 발생시킵니다."""
    # 사용자 인증
    user = authenticate(request, username=email, password=password)
    # 사용자 인증 실패 시 예외 발생
    if user is None:
        raise AuthenticationFailed('Invalid email or password')
    # 사용자 인증 성공 시 (세션) 로그인
    login(request, user)
    return user

def sign_out(request: Request):
    """로그아웃"""
    logout(request)

def get_user_jwt(user: User) -> str:
    refresh_token: RefreshToken
    refresh_token = RefreshToken.for_user(user)
    return str(refresh_token.access_token)
