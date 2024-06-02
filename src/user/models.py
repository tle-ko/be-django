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
