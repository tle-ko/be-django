from __future__ import annotations

from dataclasses import dataclass
from typing import List

from apps.activities.dto import CrewActivityDTO
from users.dto import UserDTO

from . import enums


@dataclass
class CrewMemberDTO(UserDTO):
    is_captain: bool


@dataclass
class CrewMemberCountDTO:
    count: int
    max_count: int


@dataclass
class CrewTagDTO:
    key: str
    name: str
    type: enums.CrewTagType


@dataclass
class CrewDTO:
    crew_id: int
    name: str
    icon: str
    is_active: bool
    latest_activity: CrewActivityDTO
    member_count: CrewMemberCountDTO
    tags: List[CrewTagDTO]


@dataclass
class RecruitingCrewDTO(CrewDTO):
    is_appliable: bool


@dataclass
class CrewDetailDTO(CrewDTO):
    notice: str
    members: List[CrewMemberDTO]
    activities: List[CrewActivityDTO]
    is_captain: bool
