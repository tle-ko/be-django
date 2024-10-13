from __future__ import annotations

import dataclasses
import datetime
import typing

from apps.boj.dto import BOJUserDTO
from apps.problems.dto import ProblemDTO
from apps.problems.dto import ProblemDetailDTO
from apps.problems.dto import ProblemStatisticDTO
from users.dto import UserDTO

from . import enums


@dataclasses.dataclass
class CrewSubmissionCommentDTO:
    comment_id: int
    content: str
    line_number_start: int
    line_number_end: int
    created_at: datetime.datetime
    created_by: UserDTO


@dataclasses.dataclass
class CrewSubmissionDTO:
    submission_id: int
    is_correct: bool
    submitted_at: datetime.datetime
    submitted_by: UserDTO
    reviewers: typing.List[UserDTO]


@dataclasses.dataclass
class CrewSubmissionDetailDTO(CrewSubmissionDTO):
    code: str
    comments: typing.List[CrewSubmissionCommentDTO]


@dataclasses.dataclass
class CrewProblemDTO(ProblemDTO):
    problem_id: int  # 원본 문제 ID
    order: int  # 문제 번호
    submission_id: typing.Optional[int]  # 내가 제출한 submission ID
    has_submitted: bool
    submissions: typing.List[CrewSubmissionDTO]


@dataclasses.dataclass
class CrewProblemDetailDTO(ProblemDetailDTO):
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
    problems: typing.List[CrewProblemDetailDTO]


@dataclasses.dataclass
class CrewMemberDTO(UserDTO):
    is_captain: bool


@dataclasses.dataclass
class CrewMemberCountDTO:
    count: int
    max_count: int


@dataclasses.dataclass
class CrewTagDTO:
    key: str
    name: str
    type: enums.CrewTagType


@dataclasses.dataclass
class CrewDTO:
    crew_id: int
    name: str
    icon: str
    is_active: bool
    is_recruiting: bool
    latest_activity: CrewActivityDTO
    member_count: CrewMemberCountDTO
    tags: typing.List[CrewTagDTO]


@dataclasses.dataclass
class RecruitingCrewDTO(CrewDTO):
    is_appliable: bool


@dataclasses.dataclass
class CrewDetailDTO(CrewDTO):
    notice: str
    members: typing.List[CrewMemberDTO]
    activities: typing.List[CrewActivityDTO]
    is_captain: bool


@dataclasses.dataclass
class CrewApplicantDTO(UserDTO):
    boj: BOJUserDTO


@dataclasses.dataclass
class CrewApplicationDTO:
    application_id: int
    applicant: CrewApplicantDTO
    message: str
    is_pending: bool
    is_accepted: bool
    created_at: datetime.datetime


@dataclasses.dataclass
class CrewStatisticsDTO(ProblemStatisticDTO):
    pass
