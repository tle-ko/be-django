from dataclasses import dataclass

from apps.boj.dto import BOJUserDTO


@dataclass
class UserDTO:
    user_id: int
    username: str
    profile_image: str


@dataclass
class UserDetailDTO(UserDTO):
    email: str
    boj: BOJUserDTO


@dataclass
class UserCredentialDTO(UserDTO):
    token: str
