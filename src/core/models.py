from django.db import models


class Difficulty(models.IntegerChoices):
    EASY = 1, '쉬움'
    NORMAL = 2, '보통'
    HARD = 3, '어려움'


class Tag(models.Model):
    """Data Structure & Algorithm"""
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        help_text=(
            '부모 알고리즘 태그를 입력해주세요.'
        ),
        null=True,
    )
    key = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '알고리즘 태그 키를 입력해주세요. (최대 20자)'
        ),
    )
    name_ko = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '알고리즘 태그 이름(국문)을 입력해주세요. (최대 20자)'
        ),
    )
    name_en = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '알고리즘 태그 이름(영문)을 입력해주세요. (최대 20자)'
        ),
    )


class Language(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '언어 이름을 입력해주세요. (최대 20자)'
        ),
    )
