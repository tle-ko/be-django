from django.db import models

from crews import enums


class ProgrammingLanguageChoices(models.TextChoices):
    """크루에서 사용 가능한 언어"""

    NODE_JS = enums.ProgrammingLanguage.NODE_JS.to_choice()
    KOTLIN = enums.ProgrammingLanguage.KOTLIN.to_choice()
    SWIFT = enums.ProgrammingLanguage.SWIFT.to_choice()
    CPP = enums.ProgrammingLanguage.CPP.to_choice()
    JAVA = enums.ProgrammingLanguage.JAVA.to_choice()
    PYTHON = enums.ProgrammingLanguage.PYTHON.to_choice()
    C = enums.ProgrammingLanguage.C.to_choice()
