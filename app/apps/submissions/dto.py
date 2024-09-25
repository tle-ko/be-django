from dataclasses import dataclass
from datetime import datetime

from users.dto import UserDTO


@dataclass
class SubmissionDTO:
    submission_id: int
    is_correct: bool
    submitted_at: datetime
    submitted_by: UserDTO


@dataclass
class SubmissionCommentDTO:
    comment_id: int
    content: str
    line_number_start: int
    line_number_end: int
    created_at: datetime
    created_by: UserDTO
