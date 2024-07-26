from dataclasses import dataclass
from enum import Enum


@dataclass
class _ProgrammingLanguage:
    key: str
    name: str
    extension: str

    def to_choice(self):
        return self.key, self.name


class ProgrammingLanguage(Enum):
    # TLE에서 허용중인 언어
    NODE_JS = _ProgrammingLanguage('nodejs', 'Node.js', '.js')
    KOTLIN = _ProgrammingLanguage('kotlin', 'Kotlin', '.kt')
    SWIFT = _ProgrammingLanguage('swift', 'Swift', '.swift')
    CPP = _ProgrammingLanguage('cpp', 'C++', '.cpp')
    JAVA = _ProgrammingLanguage('java', 'Java', '.java')
    PYTHON = _ProgrammingLanguage('python', 'Python', '.py')
    C = _ProgrammingLanguage('c', 'C', '.c')

    # 아직 지원하지 않는 언어
    JAVASCRIPT = _ProgrammingLanguage('javascript', 'JavaScript', '.js')
    CSHARP = _ProgrammingLanguage('csharp', 'C#', '.cs')
    RUBY = _ProgrammingLanguage('ruby', 'Ruby', '.rb')
    PHP = _ProgrammingLanguage('php', 'PHP', '.php')
