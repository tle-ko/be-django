from dataclasses import dataclass
from datetime import datetime
from typing import List

from apps.crews.enums import CrewTagType


@dataclass
class CrewDTO:
    crew_id: int
    id: int  # TODO: deprecate
    name: str
    icon: str
    is_active: bool
    is_captain: bool


@dataclass
class CrewMemberDTO:
    user_id: int
    username: str
    is_captain: bool


@dataclass
class CrewTagDTO:
    key: str
    name: str
    type: CrewTagType


@dataclass
class CrewActivityDTO:
    activity_id: int
    name: str
    date_start_at: datetime
    date_end_at: datetime


@dataclass
class CrewDashboardDTO(CrewDTO):
    notice: str
    tags: List[CrewTagDTO]
    members: List[CrewMemberDTO]
    activities: List[CrewActivityDTO]
