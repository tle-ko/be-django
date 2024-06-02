from django.db import models

from user.models import User


class Crew(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '크루 이름을 입력해주세요. (최대 20자)'
        ),
    )
    emoji = models.CharField(
        max_length=1,
        help_text=(
            '크루 아이콘을 입력해주세요. (이모지)'
        ),
        null=True,
        blank=True,
    )
    captain = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='crews',
        help_text=(
            '크루장을 입력해주세요.'
        ),
    )
    members = models.ManyToManyField(
        User,
        related_name='crews',
        help_text=(
            '크루에 속한 유저들을 입력해주세요.'
        ),
    )
    notice = models.TextField(
        help_text=(
            '크루 공지를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
