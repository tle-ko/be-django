from dataclasses import dataclass
from dataclasses import field
from typing import Tuple

from problems import models


@dataclass
class ProblemDTO:
    title: str
    description: str
    input_description: str
    output_description: str
    memory_limit: float
    time_limit: float


@dataclass(frozen=True)
class ProblemAnalysisDTO:
    time_complexity: str
    difficulty: models.ProblemDifficultyChoices
    tags: Tuple[str] = field(default_factory=tuple)
    hint: Tuple[str] = field(default_factory=tuple)
