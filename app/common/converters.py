import typing

from django.db.models import QuerySet

from users.models import User


ModelType = typing.TypeVar('ModelType')
DTOType = typing.TypeVar('DTOType')


class ModelConverter(typing.Generic[ModelType, DTOType]):
    def queryset_to_dto(self, queryset: QuerySet[ModelType]) -> typing.List[DTOType]:
        return [self.instance_to_dto(instance) for instance in queryset]

    def instance_to_dto(self, instance: ModelType) -> DTOType:
        raise NotImplementedError


class UserRequiredModelConverter(ModelConverter[ModelType, DTOType]):
    def __init__(self, user: User) -> None:
        assert isinstance(user, User)
        self.user = user
