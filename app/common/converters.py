import typing

from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet


ModelType = typing.TypeVar('ModelType')
DTOType = typing.TypeVar('DTOType')


class ModelConverter(typing.Generic[ModelType, DTOType]):
    user_required = False

    def queryset_to_dto(self, queryset: QuerySet[ModelType]) -> typing.List[DTOType]:
        return [self.instance_to_dto(instance) for instance in queryset]

    def instance_to_dto(self, instance: ModelType) -> DTOType:
        raise NotImplementedError


class AnyUserRequiredModelConverter(ModelConverter[ModelType, DTOType]):
    user_required = True

    def __init__(self, user: AbstractUser) -> None:
        assert user.is_anonymous or user.is_authenticated
        self.user = user


class AuthenticatedUserRequiredModelConverter(ModelConverter[ModelType, DTOType]):
    user_required = True

    def __init__(self, user: AbstractUser) -> None:
        assert user.is_authenticated, 'The user must be authenticated'
        self.user = user
