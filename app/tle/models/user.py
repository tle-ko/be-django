from __future__ import annotations
import typing

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from tle.models.choices import BojUserLevel

if typing.TYPE_CHECKING:
    import tle.models as _T


def get_profile_image_path(instance: User, filename: str) -> str:
    return f'user/profile/{instance.pk}/{filename}'


class UserManager(BaseUserManager):
    model: typing.Callable[..., User]

    def create(self, **kwargs):
        return self.create_user(**kwargs)

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
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
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    problems: models.ManyToManyField[_T.Problem]
    applicants: models.ManyToManyField[_T.CrewApplicant]
    members: models.ManyToManyField[_T.CrewMember]
    submissions: models.ManyToManyField[_T.Submission]
    comments: models.ManyToManyField[_T.SubmissionComment]

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
        choices=BojUserLevel.choices,
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
        # related fields
        PROBLEMS = 'problems'
        APPLICANTS = 'applicants'
        MEMBERS = 'members'
        SUBMISSIONS = 'submissions'
        COMMENTS = 'comments'
        # fields
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

    def __repr__(self) -> str:
        return f'[@{self.username}]'

    def __str__(self) -> str:
        staff = '(관리자)' if self.is_staff else ''
        return f'{self.pk} : {self.__repr__()} {staff}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
