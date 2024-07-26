from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from users.models.user_manager import UserManager
from users.models.user_boj_level import UserBojLevel


def get_profile_image_path(user: User, filename: str) -> str:
    return f'user/profile/{user.pk}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
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
        null=True,
        blank=True,
    )
    boj_level = models.IntegerField(
        help_text='백준 티어',
        choices=UserBojLevel.choices,
        null=True,
        blank=True,
        default=None,
    )
    boj_level_updated_at = models.DateTimeField(
        help_text='백준 티어 갱신 시각',
        null=True,
        blank=True,
        default=None,
    )

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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.TextField(blank=True, null=True, default=None)
    last_name = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class field_name:
        PROFILE_IMAGE = 'profile_image'
        BOJ_USERNAME = 'boj_username'
        BOJ_LEVEL = 'boj_level'
        BOJ_LEVEL_UPDATED_AT = 'boj_level_updated_at'
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
