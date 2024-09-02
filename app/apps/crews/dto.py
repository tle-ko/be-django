from dataclasses import dataclass

from apps.crews.enums import CrewTagType


@dataclass
class CrewTagDTO:
    key: str
    name: str
    type: CrewTagType
