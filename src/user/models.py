from django.contrib.auth.models import User as DjangoUser
from django.db import models


class User(DjangoUser):
    REQUIRED_FIELDS = [
        'email',
        'username',
        'password',
    ]
    image = models.ImageField(
        upload_to='user_images/',
        null=True,
        blank=True,
    )


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
