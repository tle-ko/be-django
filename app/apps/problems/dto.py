from dataclasses import dataclass
from dataclasses import field
from typing import List

from apps.analyses.dto import ProblemTagDTO
from apps.analyses.enums import ProblemDifficulty


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
class ProblemDifficultyStaticDTO:
    difficulty: ProblemDifficulty
    count: int
    ratio: float


@dataclass
class ProblemTagStaticDTO:
    tag: ProblemTagDTO
    count: int
    ratio: float


@dataclass
class ProblemStatisticDTO:
    problem_count: int = field(default=0)
    difficulties: List[ProblemDifficultyStaticDTO] = field(default_factory=list)
    tags: List[ProblemTagStaticDTO] = field(default_factory=list)
