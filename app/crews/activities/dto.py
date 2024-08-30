from dataclasses import dataclass
from datetime import datetime
from typing import List

from crews import enums
from problems.analyses.enums import ProblemDifficulty


@dataclass
class CrewProblem:
    problem_number: int
    problem_id: int
    problem_title: str
    problem_difficulty: ProblemDifficulty
    is_submitted: bool
    last_submitted_date: datetime


@dataclass
class CrewActivity:
    activity_id: int
    name: str
    start_at: datetime
    end_at: datetime
    is_in_progress: bool
    has_started: bool
    has_ended: bool


@dataclass
class SubmissionGraphNode:
    problem_number: int
    submitted_at: datetime
    is_accepted: bool  # 정답인지 여부


@dataclass
class SubmissionGraph:
    user_username: str
    user_profile_image: str
    submissions: List[SubmissionGraphNode]
