from __future__ import annotations

from django.db import models
from django.utils import timezone

from . import llms


class TextGenerationDAOManager(models.Manager):
    def create(self, prompt: str, **kwargs) -> TextGenerationDAO:
        kwargs[TextGenerationDAO.field_name.REQUEST] = prompt
        kwargs[TextGenerationDAO.field_name.CREATED_AT] = timezone.now()
        return super().create(**kwargs)


class TextGenerationDAO(models.Model):
    request = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    requested_at = models.DateTimeField(blank=True, null=True)
    responsed_at = models.DateTimeField(blank=True, null=True)
    foundation_model = models.CharField(blank=True, null=True, max_length=50)

    objects: TextGenerationDAOManager = TextGenerationDAOManager()

    class field_name:
        PK = 'pk'
        REQUEST = 'request'
        RESPONSE = 'response'
        CREATED_AT = 'created_at'
        REQUESTED_AT = 'requested_at'
        RESPONSDED_AT = 'responsed_at'
        FOUNDATION_MODEL = 'foundation_model'

    def generate(self) -> None:
        self.requested_at = timezone.now()
        self.foundation_model = llms.get_model_name()
        self.response = llms.prompt(self.request)
        self.responsed_at = timezone.now()
        self.save()
