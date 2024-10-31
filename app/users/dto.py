from dataclasses import dataclass

from apps.boj.dto import BOJUserDTO


@dataclass
class UserDTO:
    user_id: int
    username: str
    profile_image: str


@dataclass
class UserManageDTO(UserDTO):
    email: str
    boj: BOJUserDTO
