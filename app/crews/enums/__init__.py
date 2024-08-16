from enum import Enum

from django.db import models

from crews.enums.emoji import Emoji


__all__ = (
    'CrewTagType',
    'Emoji',
    'ProgrammingLanguage',
)


class CrewTagType(Enum):
    LANGUAGE = 'language'
    LEVEL = 'level'
    CUSTOM = 'custom'


class ProgrammingLanguageChoices(models.TextChoices):
    # TLE에서 허용중인 언어
    NODE_JS = 'nodejs', 'Node.js'
    KOTLIN = 'kotlin', 'Kotlin'
    SWIFT = 'swift', 'Swift'
    CPP = 'cpp', 'C++'
    JAVA = 'java', 'Java'
    PYTHON = 'python', 'Python'
    C = 'c', 'C'
    JAVASCRIPT = 'javascript', 'JavaScript'

    # 아직 지원하지 않는 언어
    CSHARP = 'csharp', 'C#'
    RUBY = 'ruby', 'Ruby'
    PHP = 'php', 'PHP'
