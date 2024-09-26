from datetime import datetime
import dataclasses
import typing

from users.dto import UserDTO


@dataclasses.dataclass
class SubmissionDTO:
    submission_id: int
    is_correct: bool
    submitted_at: datetime
    submitted_by: UserDTO
    reviewers: typing.List[UserDTO]


@dataclasses.dataclass
class SubmissionCommentDTO:
    comment_id: int
    content: str
    line_number_start: int
    line_number_end: int
    created_at: datetime
    created_by: UserDTO


@dataclasses.dataclass
class SubmissionDetailDTO(SubmissionDTO):
    code: str
    comments: typing.List[SubmissionCommentDTO] = dataclasses.field(default_factory=list)
