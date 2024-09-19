from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: int
    username: str
    profile_image: str
