from django.db.models import QuerySet

import typing


ModelType = typing.TypeVar('ModelType')
DTOType = typing.TypeVar('DTOType')


class ModelConverter(typing.Generic[ModelType, DTOType]):
    def queryset_to_dto(self, queryset: QuerySet[ModelType]) -> typing.List[DTOType]:
        return [self.instance_to_dto(instance) for instance in queryset]

    def instance_to_dto(self, instance: ModelType) -> DTOType:
        raise NotImplementedError
