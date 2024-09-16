from dataclasses import dataclass
from datetime import datetime

from apps.analyses.enums import ProblemDifficulty


@dataclass
class CrewActivityDTO:
    activity_id: int
    name: str
    start_at: datetime
    end_at: datetime
    is_in_progress: bool
    has_started: bool
    has_ended: bool


@dataclass
class CrewActivityProblemDTO:
    problem_id: int  # 문제 ID
    problem_ref_id: int  # 원본 문제 ID
    order: int # 문제 번호
    title: str
    difficulty: ProblemDifficulty


class CrewActivityProblemSubmissionDTO(CrewActivityProblemDTO):
    submission_id: int
    is_submitted: bool
    is_correct: bool
    date_submitted_at: datetime
