from __future__ import annotations

from django.db import models

from boj import enums


class BOJUser(models.Model):
    username = models.TextField(
        help_text='백준 아이디',
        max_length=40,
        unique=True,
    )
    level = models.IntegerField(
        choices=enums.BOJLevel.choices,
        default=enums.BOJLevel.U,
    )
    rating = models.IntegerField(
        default=0,
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    class field_name:
        USERNAME = 'username'
        LEVEL = 'level'
        RATING = 'rating'
        UPDATED_AT = 'updated_at'

    def __str__(self) -> str:
        return f'{self.username}'


class BOJUserSnapshot(models.Model):
    user = models.ForeignKey(
        BOJUser,
        on_delete=models.CASCADE,
    )
    level = models.IntegerField(choices=enums.BOJLevel.choices)
    rating = models.IntegerField()
    created_at = models.DateTimeField()

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
    level = models.IntegerField(choices=enums.BOJLevel.choices)
