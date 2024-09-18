from __future__ import annotations

from typing import Optional
from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet

from apps.analyses.models.proxy import ProblemAnalysis
from users.models import User

from .. import dto
from .. import models


class ProblemQuerySet(QuerySet):
    def exclude(self,
                created_by: Optional[User] = None,
                **kwargs) -> ProblemQuerySet:
        return self._kwargs_filtering(super().exclude, created_by, **kwargs)

    def filter(self,
               created_by: Optional[User] = None,
               **kwargs) -> ProblemQuerySet:
        return self._kwargs_filtering(super().filter, created_by, **kwargs)

    def created_by(self, user: User) -> ProblemQuerySet:
        return self.filter(created_by=user)

    def search(self, q: Optional[str] = None) -> ProblemQuerySet:
        if q is None:
            return self
        return self.filter(**{
            Problem.field_name.TITLE+'__icontains': q,
        }).order_by(Problem.field_name.TITLE)

    def _kwargs_filtering(self,
                          filter_function,
                          created_by: Optional[User] = None,
                          **kwargs) -> ProblemQuerySet:
        if created_by is not None:
            assert isinstance(created_by, User)
            kwargs[models.ProblemDAO.field_name.CREATED_BY] = created_by
        return filter_function(**kwargs)


class Problem(models.ProblemDAO):
    objects: Union[ProblemQuerySet, QuerySet[Problem]]
    objects = Manager.from_queryset(ProblemQuerySet)()

    class Meta:
        proxy = True

    def analysis(self) -> dto.ProblemAnalysisDTO:
        try:
            return ProblemAnalysis.objects.get_by_problem(self).as_dto()
        except ProblemAnalysis.DoesNotExist:
            return dto.ProblemAnalysisDTO.none(self.pk)

    def as_dto(self) -> dto.ProblemDTO:
        return dto.ProblemDTO(
            problem_id=self.pk,
            title=self.title,
            analysis=self.analysis(),
        )

    def as_detail_dto(self) -> dto.ProblemDetailDTO:
        return dto.ProblemDetailDTO(
            **self.as_dto().__dict__,
            description=self.description,
            input_description=self.input_description,
            output_description=self.output_description,
            memory_limit=dto.ProblemLimitDTO.mega_byte(self.memory_limit),
            time_limit=dto.ProblemLimitDTO.second(self.time_limit),
        )
