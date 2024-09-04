from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Tuple

from apps.problems.analyses.enums import ProblemDifficulty


@dataclass
class ProblemAnalysisDTO:
    problem_id: int
    time_complexity: str
    difficulty: ProblemDifficulty
    tags: Tuple[str] = field(default_factory=tuple)
    hints: Tuple[str] = field(default_factory=tuple)


@dataclass
class ProblemTagDTO:
    key: str
    name_ko: str
    name_en: str

    def __hash__(self) -> int:
        return hash(self.key)
