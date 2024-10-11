from __future__ import annotations

from django.conf import settings
from google import generativeai as genai


def get_model_name() -> str:
    return Gemini.model_name


def prompt(prompt: str) -> str:
    return Gemini().perform_prompt(prompt)


class FoundationModel:
    model_name = '<REPLACE_THIS>'

    def perform_prompt(self, prompt: str) -> str:
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

    def perform_prompt(self, prompt: str) -> None:
        return self.chat.send_message(content=prompt).text
