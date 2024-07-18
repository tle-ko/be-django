from dataclasses import dataclass
from typing import List


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
    difficulty: str
    tags: List[str]
    hint: List[str]
