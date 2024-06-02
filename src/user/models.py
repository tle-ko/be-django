from django.contrib import auth
from django.db import models


class User(auth.models.User):
    REQUIRED_FIELDS = [
        'email',
        'username',
        'password',
    ]

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    image = models.ImageField(
        upload_to='user_images/',
        null=True
    )
    boj_id = models.CharField(
        max_length=100, # TODO: 추후 조사 필요
        unique=True,
        help_text=(
            '백준 아이디를 입력해주세요.'
        ),
        null=True,
    )
