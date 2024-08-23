from dataclasses import dataclass

from boj import enums


@dataclass(frozen=True)
class BOJUserData:
    level: enums.BOJLevel
    rating: int
