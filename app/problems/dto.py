from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from dataclasses import field
from typing import Tuple

from problems import enums
from problems import models


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

    @classmethod
    def from_model(self, instance: models.Problem) -> ProblemDTO:
        return ProblemDTO(
            id=instance.pk,
            title=instance.title,
            description=instance.description,
            input_description=instance.input_description,
            output_description=instance.output_description,
            memory_limit=instance.memory_limit,
            time_limit=instance.time_limit,
        )


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

    @classmethod
    def from_model(self, instance: models.ProblemTag) -> ProblemTagDTO:
        return ProblemTagDTO(
            key=instance.key,
            name_ko=instance.name_ko,
            name_en=instance.name_en,
        )


@dataclass
class ProblemStatisticDTO:
    sample_count: int = field(default=0)
    difficulty: Counter[int] = field(default_factory=Counter)
    tags: Counter[ProblemTagDTO] = field(default_factory=Counter)
