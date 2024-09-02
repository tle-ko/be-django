from __future__ import annotations

from typing import Optional
from typing import Tuple

from django.db import models
from django.db.models import Manager

from apps.boj.enums import BOJLevel
from users.models import User


class BOJUserManager(Manager):
    def filter(self, username: Optional[str] = None, *args, **kwargs) -> models.QuerySet[BOJUser]:
        if username is not None:
            kwargs[User.field_name.USERNAME] = username
        return super().filter(*args, **kwargs)

    def get_or_create_by_username(self, username: str) -> Tuple[BOJUser, bool]:
        return self.get_or_create(**{BOJUser.field_name.USERNAME: username})

    def get_by_username(self, username: str) -> BOJUser:
        return self.get_or_create_by_username(username)[0]


class BOJUser(models.Model):
    username = models.TextField(
        help_text='백준 아이디',
        max_length=40,
        unique=True,
    )
    level = models.IntegerField(
        choices=BOJLevel.choices,
        default=BOJLevel.U,
    )
    rating = models.IntegerField(
        default=0,
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    objects: BOJUserManager = BOJUserManager()

    class field_name:
        USERNAME = 'username'
        LEVEL = 'level'
        RATING = 'rating'
        UPDATED_AT = 'updated_at'

    def __str__(self) -> str:
        return f'{self.username}'


class BOJUserSnapshotManager(Manager):
    def create_snapshot_of(self, boj_user: BOJUser) -> BOJUserSnapshot:
        return self.create(**{
            BOJUserSnapshot.field_name.USER: boj_user,
            BOJUserSnapshot.field_name.LEVEL: boj_user.level,
            BOJUserSnapshot.field_name.RATING: boj_user.rating,
            BOJUserSnapshot.field_name.CREATED_AT: boj_user.updated_at,
        })


class BOJUserSnapshot(models.Model):
    user = models.ForeignKey(
        BOJUser,
        on_delete=models.CASCADE,
    )
    level = models.IntegerField(choices=BOJLevel.choices)
    rating = models.IntegerField()
    created_at = models.DateTimeField()

    objects: BOJUserSnapshotManager = BOJUserSnapshotManager()

    class field_name:
        USER = 'user'
        LEVEL = 'level'
        RATING = 'rating'
        CREATED_AT = 'created_at'


class BOJProblem(models.Model):
    title = models.TextField()
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    memory_limit = models.FloatField()
    time_limit = models.FloatField()
    tags = models.JSONField(default=list)
    level = models.IntegerField(choices=BOJLevel.choices)
