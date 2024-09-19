from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple

from . import enums


@dataclass
class ProblemAnalysisRawDTO:
    problem_id: int
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
        return hash(self.key)


@dataclass
class ProblemDifficultyDTO:
    value: int
    name_ko: str
    name_en: str

    @staticmethod
    def none() -> ProblemDifficultyDTO:
        return ProblemDifficultyDTO(enums.ProblemDifficulty.UNDER_ANALYSIS)

    def __init__(self, difficulty: enums.ProblemDifficulty):
        self.value = difficulty.value
        self.name_ko = difficulty.get_name(lang='ko')
        self.name_en = difficulty.get_name(lang='en')


@dataclass
class ProblemAnalysisDTO:
    problem_id: int
    is_analyzed: bool
    time_complexity: str
    difficulty: ProblemDifficultyDTO
    hints: List[str] = field(default_factory=list)
    tags: List[ProblemTagDTO] = field(default_factory=list)

    @staticmethod
    def none(problem_id: int) -> ProblemAnalysisDTO:
        return ProblemAnalysisDTO(
            problem_id=problem_id,
            is_analyzed=False,
            time_complexity='',
            difficulty=ProblemDifficultyDTO.none(),
            hints=[],
            tags=[],
        )
