from apps.boj.converters import BOJUserConverter
from common.converters import ModelConverter

from . import dto
from . import models


class UserConverter(ModelConverter[models.User, dto.UserDTO]):
    def instance_to_dto(self, instance: models.User) -> dto.UserDTO:
        return dto.UserDTO(
            user_id=instance.pk,
            username=instance.username,
            profile_image=self._profile_image(instance),
        )

    def _profile_image(self, instance: models.User):
        return instance.profile_image.url if instance.profile_image else None

    def instance_to_manage_dto(self, instance: models.User) -> dto.UserManageDTO:
        return dto.UserManageDTO(
            **self.instance_to_dto(instance).__dict__,
            email=instance.email,
            boj=BOJUserConverter().username_to_dto(instance.boj_username),
        )
