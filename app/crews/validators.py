from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from crews.enums import Emoji


class EmojiValidator(BaseValidator):
    def __init__(self, message: str = None) -> None:
        self.message = message

    def __call__(self, value) -> None:
        try:
            Emoji(value)  # just checking if it's valid emoji
        except ValueError:
            raise ValidationError(self.message, params={"value": value})
