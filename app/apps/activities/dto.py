from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List


@dataclass
class UserDTO:
    user_id: int
    username: str
    profile_image: str


@dataclass
class UserSubmissionTableDTO:
    submissions: List[UserSubmissionTableRowDTO]
    submitted_by: UserDTO


@dataclass
class UserSubmissionTableRowDTO:
    submission_id: int
    problem_id: str
    problem_title: str
    problem_order: int
    reviewers: List[UserDTO]
    created_at: datetime
    is_submitted: bool
