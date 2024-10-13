from apps.boj.converters import BOJUserConverter
from common.converters import ModelConverter

from . import dto
from . import models


class UserConverter(ModelConverter[models.User, dto.UserDTO]):
    def instance_to_dto(self, instance: models.User) -> dto.UserDTO:
        return dto.UserDTO(
            user_id=instance.pk,
            username=instance.username,
            profile_image=instance.get_profile_image_url(),
        )


class UserDetailConverter(ModelConverter[models.User, dto.UserDetailDTO]):
    def instance_to_dto(self, instance: models.User) -> dto.UserDetailDTO:
        return dto.UserDetailDTO(
            **UserConverter().instance_to_dto(instance).__dict__,
            email=instance.email,
            boj=BOJUserConverter().username_to_dto(instance.boj_username),
        )


class UserCredentialConverter(ModelConverter[models.User, dto.UserCredentialDTO]):
    def instance_to_dto(self, instance: models.User) -> dto.UserCredentialDTO:
        return dto.UserCredentialDTO(
            **UserConverter().instance_to_dto(instance).__dict__,
            token=instance.token,
        )
