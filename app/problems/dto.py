from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from dataclasses import field
from typing import Tuple

from problems import enums
from problems import models


@dataclass
class ProblemDTO:
    title: str
    description: str
    input_description: str
    output_description: str
    memory_limit: float
    time_limit: float


@dataclass
class ProblemAnalysisDTO:
    time_complexity: str
    difficulty: enums.ProblemDifficulty
    tags: Tuple[str] = field(default_factory=tuple)
    hints: Tuple[str] = field(default_factory=tuple)


@dataclass
class ProblemTagDTO:
    key: str
    name_ko: str
    name_en: str

    def __hash__(self) -> int:
        return self.key


@dataclass
class ProblemStatisticDTO:
    sample_count: int = field(default=0)
    difficulty: Counter[int] = field(default_factory=Counter)
    tags: Counter[ProblemTagDTO] = field(default_factory=Counter)
