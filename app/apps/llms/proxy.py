from __future__ import annotations

from typing import Union

from django.db.models import Manager

from . import models
from . import llms



class TextGenerationManager(Manager):
    def create(self, request: str) -> TextGeneration:
        kwargs = {}
        kwargs[TextGeneration.field_name.REQUEST] = request
        return super().create(**kwargs)


class TextGeneration(models.TextGenerationDAO):
    objects: Union[Manager[TextGeneration], TextGenerationManager]
    objects = TextGenerationManager()

    class Meta:
        proxy = True

    def generate(self) -> None:
        llms.Gemini().generate(self)
