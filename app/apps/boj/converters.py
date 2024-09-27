from common.converters import ModelConverter

from . import dto
from . import models


class BOJUserConverter(ModelConverter[models.BOJUserDAO, dto.BOJUserDTO]):
    def instance_to_dto(self, instance: models.BOJUserDAO) -> dto.BOJUserDTO:
        return dto.BOJUserDTO(
            username=instance.username,
            profile_url=f'https://boj.kr/{instance.username}',
            level=dto.BOJLevelDTO(instance.level),
            rating=instance.rating,
            updated_at=instance.updated_at,
        )

    def username_to_dto(self, username: str) -> dto.BOJUserDTO:
        instance = models.BOJUserDAO.objects.get_or_create(**{
            models.BOJUserDAO.field_name.USERNAME: username,
        })[0]
        return self.instance_to_dto(instance)
