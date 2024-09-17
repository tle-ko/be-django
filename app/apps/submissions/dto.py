from dataclasses import dataclass
from datetime import datetime

from users.dto import UserDTO


@dataclass
class SubmissionDTO:
    submission_id: int
    is_correct: bool
    submitted_at: datetime
    submitted_by: UserDTO
