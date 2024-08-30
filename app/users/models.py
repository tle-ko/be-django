from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


def get_profile_image_path(user: User, filename: str) -> str:
    return f'user/profile/{user.pk}/{filename}'


def default_expires_at_factory():
    return timezone.now() + timedelta(minutes=5)


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

    def get_by_username(self, username: str) -> User:
        return self.get(**{User.field_name.BOJ_USERNAME: username})

    def create_user(self, email: str, username: str, password: str, **extra_fields):
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create(email, username, password, **extra_fields)


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
        PROFILE_IMAGE = 'profile_image'
        BOJ_USERNAME = 'boj_username'
        USERNAME = 'username'
        EMAIL = 'email'
        PASSWORD = 'password'
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


class UserEmailVerification(models.Model):
    email = models.EmailField(
        help_text='이메일 주소',
        primary_key=True,
    )
    verification_code = models.TextField(
        help_text='인증 코드',
        null=False,
        blank=False,
    )
    verification_token = models.TextField(
        help_text='인증 토큰',
        null=True,
        blank=True,
    )
    expires_at = models.DateTimeField(default=default_expires_at_factory)
    created_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        EMAIL = 'email'
        VERIFICATION_CODE = 'verification_code'
        VERIFICATION_TOKEN = 'verification_token'
        EXPIRES_AT = 'expires_at'
        CREATED_AT = 'created_at'

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()
