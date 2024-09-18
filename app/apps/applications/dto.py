from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from apps.boj.dto import BOJUserDTO
from apps.boj.models.proxy import BOJUser
from users.dto import UserDTO
from users.models import User


@dataclass
class CrewApplicantDTO(UserDTO):
    boj: BOJUserDTO

    @staticmethod
    def from_user(user: User):
        return CrewApplicantDTO(
            **user.as_dto().__dict__,
            boj=BOJUser.objects.get_or_create(user.username).as_dto(),
        )


@dataclass
class CrewApplicationDTO:
    application_id: int
    applicant: CrewApplicantDTO
    message: str
    is_pending: bool
    is_accepted: bool
    created_at: datetime


@dataclass
class ReviewedCrewApplicationDTO(CrewApplicationDTO):
    reviewed_at: datetime
    reviewed_by: UserDTO
