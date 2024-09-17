from __future__ import annotations

from dataclasses import dataclass
from typing import List

from apps.activities.dto import CrewActivityDTO
from users.dto import UserDTO

from . import enums


@dataclass
class CrewDTO:
    crew_id: int
    name: str
    icon: str
    is_active: bool
    latest_activity: CrewActivityDTO


@dataclass
class CrewTagDTO:
    key: str
    name: str
    type: enums.CrewTagType


@dataclass
class CrewMemberDTO(UserDTO):
    is_captain: bool


@dataclass
class CrewDashboardDTO(CrewDTO):
    captain: CrewMemberDTO
    notice: str
    tags: List[CrewTagDTO]
    members: List[CrewMemberDTO]
    activities: List[CrewActivityDTO]
