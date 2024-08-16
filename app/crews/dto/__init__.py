from collections import Counter
from dataclasses import dataclass
from dataclasses import field
from typing import Counter
from typing import List


from crews.enums import CrewTagType


@dataclass
class ProblemTag:
    key: str
    name_ko: str
    name_en: str

    def __hash__(self) -> int:
        return self.key


@dataclass
class ProblemStatistic:
    sample_count: int = field(default=0)
    difficulty: Counter[int] = field(default_factory=Counter)
    tags: Counter[ProblemTag] = field(default_factory=Counter)


@dataclass
class CrewTag:
    key: str
    name: str
    type: CrewTagType


@dataclass
class CrewProblem:
    id: int
