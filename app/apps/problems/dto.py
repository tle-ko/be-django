from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from apps.analyses.dto import ProblemAnalysisDTO
from apps.analyses.dto import ProblemTagDTO
from apps.analyses.enums import ProblemDifficulty

from . import enums


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
    problem_count: int
    difficulties: List[ProblemDifficultyStaticDTO]
    tags: List[ProblemTagStaticDTO]
