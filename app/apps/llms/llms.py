from django.conf import settings
from django.utils import timezone
from google import generativeai as genai

from . import models


class FoundationModel:
    model_name = '<REPLACE_THIS>'

    def generate(self, obj: models.TextGenerationDAO) -> None:
        obj.requested_at = timezone.now()
        obj.foundation_model = self.__class__.model_name
        self.perform_generate(obj)
        obj.responsed_at = timezone.now()
        obj.save()

    def perform_generate(self, obj: models.TextGenerationDAO) -> None:
        raise NotImplementedError


# Gemini

genai.configure(api_key=settings.GEMINI_API_KEY)


class Gemini(FoundationModel):
    model_name = "gemini-1.5-flash"

    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )
        self.chat = self.model.start_chat(history=[])

    def perform_generate(self, obj: models.TextGenerationDAO) -> None:
        obj.response = self.chat.send_message(content=obj.request).text
