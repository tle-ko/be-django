from django.db import models

from crews import enums
from crews.models.crew import Crew


class CrewSubmittableLanguage(models.Model):
    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
    )
    language = models.TextField(
        choices=enums.ProgrammingLanguageChoices.choices,
        help_text='언어 키를 입력해주세요. (최대 20자)',
    )

    class field_name:
        CREW = 'crew'
        LANGUAGE = 'language'

    class Meta:
        ordering = ['crew']

    def __str__(self) -> str:
        return f'[{self.pk} : #{self.language}]'
