from django.db import models


class SubmissionLanguage(models.Model):
    key = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '언어 키를 입력해주세요. (최대 20자)'
        ),
    )
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text=(
            '언어 이름을 입력해주세요. (최대 20자)'
        ),
    )
    extension = models.CharField(
        max_length=20,
        help_text=(
            '언어 확장자를 입력해주세요. (최대 20자)'
        ),
    )

    def __repr__(self) -> str:
        return f'[#{self.key}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ({self.name})'
