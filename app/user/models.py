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
        validators=[
            # TODO: 이미지 크기 제한
            # TODO: 이미지 확장자 제한
        ]
    )

    def __repr__(self) -> str:
        return f'[@{self.username}]'

    def __str__(self) -> str:
        staff = '(관리자)' if self.is_staff else ''
        return f'{self.pk} : {self.__repr__()} {staff}'


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
