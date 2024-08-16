from dataclasses import dataclass
from enum import Enum

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


class ProgrammingLanguage(Enum):
    @dataclass
    class Item:
        key: str
        name: str
        extension: str

    # TLE에서 허용중인 언어
    NODE_JS = Item('nodejs', 'Node.js', '.js')
    KOTLIN = Item('kotlin', 'Kotlin', '.kt')
    SWIFT = Item('swift', 'Swift', '.swift')
    CPP = Item('cpp', 'C++', '.cpp')
    JAVA = Item('java', 'Java', '.java')
    PYTHON = Item('python', 'Python', '.py')
    C = Item('c', 'C', '.c')

    # 아직 지원하지 않는 언어
    JAVASCRIPT = Item('javascript', 'JavaScript', '.js')
    CSHARP = Item('csharp', 'C#', '.cs')
    RUBY = Item('ruby', 'Ruby', '.rb')
    PHP = Item('php', 'PHP', '.php')

    def to_choice(self):
        return self.value.key, self.value.name
