from django.db import models

from crews.enums import ProgrammingLanguage


class ProgrammingLanguageChoices(models.TextChoices):
    """크루에서 사용 가능한 언어"""

    NODE_JS = ProgrammingLanguage.NODE_JS.value.to_choice()
    KOTLIN = ProgrammingLanguage.KOTLIN.value.to_choice()
    SWIFT = ProgrammingLanguage.SWIFT.value.to_choice()
    CPP = ProgrammingLanguage.CPP.value.to_choice()
    JAVA = ProgrammingLanguage.JAVA.value.to_choice()
    PYTHON = ProgrammingLanguage.PYTHON.value.to_choice()
    C = ProgrammingLanguage.C.value.to_choice()
