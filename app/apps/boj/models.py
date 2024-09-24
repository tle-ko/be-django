from django.db import models

from . import enums


class BOJUserDAO(models.Model):
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


class BOJUserSnapshotDAO(models.Model):
    user = models.ForeignKey(
        BOJUserDAO,
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


class BOJProblemDAO(models.Model):
    title = models.TextField()
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    memory_limit = models.FloatField()
    time_limit = models.FloatField()
    time_limit_description = models.TextField(default='')
    tags = models.JSONField(default=list)
    level = models.IntegerField(choices=enums.BOJLevel.choices)

    class field_name:
        PK = 'pk'
        TITLE = 'title'
        DESCRIPTION = 'description'
        INPUT_DESCRIPTION = 'input_description'
        OUTPUT_DESCRIPTION = 'output_description'
        MEMORY_LIMIT = 'memory_limit'
        TIME_LIMIT = 'time_limit'
        TIME_LIMIT_DESCRIPTION = 'time_limit_description'
        TAGS = 'tags'
        LEVEL = 'level'

    class Meta:
        ordering = ['pk']


class BOJTagDAO(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 키를 입력해주세요. (최대 20자)',
    )
    name_ko = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(국문)을 입력해주세요. (최대 50자)',
    )
    name_en = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(영문)을 입력해주세요. (최대 50자)',
    )

    class field_name:
        KEY = 'key'
        NAME_KO = 'name_ko'
        NAME_EN = 'name_en'

    class Meta:
        ordering = ['key']

    def __repr__(self) -> str:
        return f'[#{self.key}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ({self.name_ko})'


class BOJTagRelationDAO(models.Model):
    parent = models.ForeignKey(
        BOJTagDAO,
        on_delete=models.CASCADE,
        related_name='parent'
    )
    child = models.ForeignKey(
        BOJTagDAO,
        on_delete=models.CASCADE,
        related_name='child'
    )

    class field_name:
        PK = 'pk'
        PARENT = 'parent'
        CHILD = 'child'

    def __str__(self) -> str:
        return f'{self.pk} : #{self.parent.key} <- #{self.child.key}'
