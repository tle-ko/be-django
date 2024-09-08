from collections import Counter
from dataclasses import dataclass
from dataclasses import field

from apps.analyses.dto import ProblemTagDTO


@dataclass
class ProblemDTO:
    id: int
    title: str
    description: str
    input_description: str
    output_description: str
    memory_limit: float
    time_limit: float

    def __str__(self) -> str:
        return f'<ProblemDTO id={self.id} title="{self.title}">'


@dataclass
class ProblemStatisticDTO:
    sample_count: int = field(default=0)
    difficulty: Counter[int] = field(default_factory=Counter)
    tags: Counter[ProblemTagDTO] = field(default_factory=Counter)
