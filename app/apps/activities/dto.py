from __future__ import annotations

import dataclasses
import datetime
import typing

from apps.problems.dto import ProblemDTO
from apps.problems.dto import ProblemDetailDTO
from apps.submissions.dto import SubmissionDTO


@dataclasses.dataclass
class CrewActivityProblemDTO(ProblemDTO):
    problem_id: int  # 원본 문제 ID
    order: int  # 문제 번호
    submission_id: typing.Optional[int]  # 내가 제출한 submission ID
    has_submitted: bool
    submissions: typing.List[SubmissionDTO]


@dataclasses.dataclass
class CrewActivityProblemDetailDTO(ProblemDetailDTO):
    problem_id: int  # 원본 문제 ID
    order: int  # 문제 번호
    submission_id: typing.Optional[int]  # 내가 제출한 submission ID
    has_submitted: bool


@dataclasses.dataclass
class CrewActivityDTO:
    activity_id: int
    name: str
    start_at: datetime.datetime
    end_at: datetime.datetime
    is_in_progress: bool
    has_started: bool
    has_ended: bool


@dataclasses.dataclass
class CrewActivityDetailDTO(CrewActivityDTO):
    problems: typing.List[CrewActivityProblemDetailDTO]
