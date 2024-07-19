from django.db import models


class ProblemTag(models.Model):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        help_text=(
            '부모 알고리즘 태그를 입력해주세요.'
        ),
        null=True,
        blank=True,
    )
    key = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            '알고리즘 태그 키를 입력해주세요. (최대 20자)'
        ),
    )
    name_ko = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            '알고리즘 태그 이름(국문)을 입력해주세요. (최대 50자)'
        ),
    )
    name_en = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            '알고리즘 태그 이름(영문)을 입력해주세요. (최대 50자)'
        ),
    )

    class field_name:
        PARENT = 'parent'
        KEY = 'key'
        NAME_KO = 'name_ko'
        NAME_EN = 'name_en'

    class Meta:
        ordering = ['key']

    def __repr__(self) -> str:
        return f'[#{self.key}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ({self.name_ko})'
