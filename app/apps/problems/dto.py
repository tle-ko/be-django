from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from apps.boj.dto import BOJTagDTO

from . import enums


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
    tags: List[BOJTagDTO] = field(default_factory=list)

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


@dataclass
class ProblemDTO:
    problem_id: int
    title: str
    analysis: ProblemAnalysisDTO


@dataclass
class UnitDTO:
    name: str
    value: str

    def __init__(self, unit: enums.Unit):
        self.name = unit.label
        self.value = unit.value


@dataclass
class ProblemLimitDTO:
    value: float
    unit: UnitDTO

    @staticmethod
    def second(value: float) -> ProblemLimitDTO:
        return ProblemLimitDTO(value=value, unit=UnitDTO(enums.Unit.SECOND))

    @staticmethod
    def mega_byte(value: float) -> ProblemLimitDTO:
        return ProblemLimitDTO(value=value, unit=UnitDTO(enums.Unit.MEGA_BYTE))


@dataclass
class ProblemDetailDTO(ProblemDTO):
    link: str
    description: str
    input_description: str
    output_description: str
    memory_limit: ProblemLimitDTO
    time_limit: ProblemLimitDTO
    created_at: datetime


@dataclass
class ProblemDifficultyStaticDTO:
    difficulty: enums.ProblemDifficulty
    count: int
    ratio: float


@dataclass
class ProblemTagStaticDTO:
    tag: BOJTagDTO
    count: int
    ratio: float


@dataclass
class ProblemStatisticDTO:
    problem_count: int
    difficulties: List[ProblemDifficultyStaticDTO]
    tags: List[ProblemTagStaticDTO]
