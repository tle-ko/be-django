from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Optional

from apps.problems.dto import ProblemDTO
from apps.problems.dto import ProblemDetailDTO
from apps.submissions.dto import SubmissionDTO


@dataclass
class CrewActivityProblemDTO(ProblemDTO):
    problem_ref_id: int  # 원본 문제 ID
    order: int  # 문제 번호


@dataclass
class CrewActivityProblemDetailDTO(ProblemDetailDTO):
    problem_ref_id: int  # 원본 문제 ID
    order: int  # 문제 번호


@dataclass
class CrewActivityProblemExtraDetailDTO(CrewActivityProblemDTO):
    submissions: List[SubmissionDTO]
    my_submission: Optional[SubmissionDTO]


@dataclass
class CrewActivityDTO:
    activity_id: int
    name: str
    start_at: datetime
    end_at: datetime
    is_in_progress: bool
    has_started: bool
    has_ended: bool

    @staticmethod
    def none(name: str) -> CrewActivityDTO:
        return CrewActivityDTO(
            activity_id=None,
            name=name,
            start_at=None,
            end_at=None,
            is_in_progress=False,
            has_started=False,
            has_ended=False,
        )


@dataclass
class CrewActivityDetailDTO(CrewActivityDTO):
    problems: List[CrewActivityProblemDTO]


@dataclass
class CrewActivityExtraDetailDTO(CrewActivityDTO):
    problems: List[CrewActivityProblemExtraDetailDTO]
