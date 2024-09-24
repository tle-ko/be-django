from dataclasses import dataclass
from datetime import datetime
from typing import Union

from . import enums


@dataclass
class BOJLevelDTO:
    value: int
    name: str

    def __init__(self, level: Union[enums.BOJLevel, int]):
        level = enums.BOJLevel(level)
        self.value = level.value
        self.name = level.get_name()


@dataclass
class BOJUserDTO:
    username: str
    profile_url: str
    level: BOJLevelDTO
    rating: int
    updated_at: datetime


@dataclass
class BOJTagDTO:
    key: str
    name_ko: str
    name_en: str

    def __hash__(self) -> int:
        return hash(self.key)
