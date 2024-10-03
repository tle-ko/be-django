from __future__ import annotations

from datetime import timedelta
from hashlib import sha256
from random import randint
from typing import Iterable, Optional

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from . import dto


def get_profile_image_path(user: User, filename: str) -> str:
    return f'user/profile/{user.pk}/{filename}'


class UserManager(BaseUserManager):
    def create(self, email: str, username: str, password: str, **kwargs) -> User:
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = User(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, *args, **kwargs):
        instance = self.create(*args, **kwargs)
        return instance

    def create_superuser(self, *args, **kwargs):
        instance = self.create(*args, **kwargs)
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
        return instance

    def filter(self,
               email: Optional[str] = None,
               username: Optional[str] = None,
               *args,
               **kwargs) -> models.QuerySet[User]:
        if email is not None:
            kwargs[User.field_name.EMAIL] = email
        if username is not None:
            kwargs[User.field_name.USERNAME] = username
        return super().filter(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='username',
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    profile_image = models.ImageField(
        help_text='프로필 이미지',
        upload_to=get_profile_image_path,
        null=True,
        blank=True,
        validators=[
            # TODO: 이미지 크기 제한
            # TODO: 이미지 확장자 제한
        ]
    )
    boj_username = models.CharField(
        help_text='백준 아이디',
        max_length=40,
    )
    token = models.TextField(null=True, blank=True, default=None)
    refresh_token = models.TextField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.TextField(blank=True, null=True, default=None)
    last_name = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    objects: UserManager = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class field_name:
        PK = 'pk'
        PROFILE_IMAGE = 'profile_image'
        USERNAME = 'username'
        EMAIL = 'email'
        PASSWORD = 'password'
        BOJ_USERNAME = 'boj_username'
        TOKEN = 'token'
        REFRESH_TOKEN = 'refresh_token'
        IS_ACTIVE = 'is_active'
        IS_STAFF = 'is_staff'
        IS_SUPERUSER = 'is_superuser'
        FIRST_NAME = 'first_name'
        LAST_NAME = 'last_name'
        CREATED_AT = 'created_at'
        LAST_LOGIN = 'last_login'

    @property
    def date_joined(self):
        return self.created_at

    def __str__(self) -> str:
        return f'[{self.pk} : "{self.username}"]' + (' (관리자)' if self.is_staff else '')

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_url(self) -> Optional[str]:
        return self.profile_image.url if self.profile_image else None

    def rotate_token(self):
        token: RefreshToken = RefreshToken.for_user(self)
        self.token = str(token.access_token)
        self.refresh_token = token.token


class UserEmailVerificationManager(BaseUserManager):
    def get_or_create_by_email(self, email: str) -> UserEmailVerification:
        return super().get_or_create(**{UserEmailVerification.field_name.EMAIL: email})[0]


class UserEmailVerification(models.Model):
    email = models.EmailField(
        help_text='이메일 주소',
        primary_key=True,
    )
    verification_code = models.TextField(
        help_text='인증 코드',
        null=True,
        blank=True,
    )
    verification_token = models.TextField(
        help_text='인증 토큰',
        null=True,
        blank=True,
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects: UserEmailVerificationManager = UserEmailVerificationManager()

    class field_name:
        EMAIL = 'email'
        VERIFICATION_CODE = 'verification_code'
        VERIFICATION_TOKEN = 'verification_token'
        EXPIRES_AT = 'expires_at'
        CREATED_AT = 'created_at'

    def is_expired(self) -> bool:
        return (self.expires_at is None) or self.expires_at < timezone.now()

    def is_valid_code(self, code: str, raise_exception=False) -> bool:
        try:
            assert isinstance(code, str), '올바르지 않은 형식입니다.'
            assert code, '인증 코드가 비어있습니다.'
            assert not self.is_expired(), '인증 코드가 만료되었습니다.'
            assert self.verification_code == code, '인증 코드가 일치하지 않습니다.'
        except AssertionError as exception:
            if raise_exception:
                raise ValidationError(exception)
            return False
        else:
            return True

    def revoke_code(self):
        self.verification_code = None
        self.expires_at = None

    def revoke_token(self):
        self.verification_token = None

    def rotate_code(self, code_len: int = 6):
        self.verification_code = self._create_code(code_len)
        self.expires_at = timezone.now() + timedelta(minutes=5)

    def rotate_token(self, seed: Optional[str] = None):
        if seed is None:
            seed = self._create_code(code_len=16)
        self.verification_token = sha256(seed.encode()).hexdigest()

    def _create_code(self, code_len: int) -> str:
        return ''.join(chr(randint(ord('A'), ord('Z'))) for _ in range(code_len))
