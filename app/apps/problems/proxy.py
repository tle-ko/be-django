from __future__ import annotations

from typing import List
from typing import Optional
from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.dispatch import receiver

from apps.boj.proxy import BOJTag
from users.models import User

from . import analyzer
from . import dto
from . import enums
from . import models


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

    def as_dto(self: QuerySet[Problem]) -> List[dto.ProblemDTO]:
        return [problem.as_dto() for problem in self]

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

    def analyze(self) -> ProblemAnalysis:
        analyzer.schedule_analysis(self.pk)

    def as_dto(self) -> dto.ProblemDTO:
        return dto.ProblemDTO(
            problem_id=self.pk,
            title=self.title,
            analysis=self.analysis(),
        )

    def as_detail_dto(self) -> dto.ProblemDetailDTO:
        return dto.ProblemDetailDTO(
            **self.as_dto().__dict__,
            link=self.link,
            description=self.description,
            input_description=self.input_description,
            output_description=self.output_description,
            memory_limit=dto.ProblemLimitDTO.mega_byte(self.memory_limit),
            time_limit=dto.ProblemLimitDTO.second(self.time_limit),
            created_at=self.created_at,
        )


@receiver(post_save, sender=models.ProblemDAO)
def on_problem_created(sender, instance: models.ProblemDAO, created: bool, **kwargs):
    if created:
        analyzer.schedule_analysis(instance.pk)


class ProblemAnalysisQuerySet(QuerySet):
    def exclude(self,
                problem: models.ProblemDAO = None,
                *args,
                **kwargs) -> ProblemAnalysisQuerySet:
        return self._kwargs_filtering(super().exclude, problem, *args, **kwargs)

    def filter(self,
               problem: models.ProblemDAO = None,
               *args,
               **kwargs) -> ProblemAnalysisQuerySet:
        return self._kwargs_filtering(super().filter, problem, *args, **kwargs)

    def get_by_problem(self, problem: models.ProblemDAO) -> ProblemAnalysis:
        return self.problem(problem).latest()

    def problem(self, problem: models.ProblemDAO) -> ProblemAnalysisQuerySet:
        return self.filter(problem=problem)

    def create_from_dto(self, analysis_dto: dto.ProblemAnalysisRawDTO) -> ProblemAnalysis:
        analysis = ProblemAnalysis(**{
            ProblemAnalysis.field_name.PROBLEM: models.ProblemDAO.objects.get(pk=analysis_dto.problem_id),
            ProblemAnalysis.field_name.TIME_COMPLEXITY: analysis_dto.time_complexity,
            ProblemAnalysis.field_name.DIFFICULTY: analysis_dto.difficulty,
            ProblemAnalysis.field_name.HINTS: analysis_dto.hints,
        })
        analysis_tags = []
        for tag_key in analysis_dto.tags:
            tag = BOJTag.objects.get_by_key(tag_key)
            analysis_tag = ProblemAnalysisTag(**{
                ProblemAnalysisTag.field_name.ANALYSIS: analysis,
                ProblemAnalysisTag.field_name.TAG: tag,
            })
            analysis_tags.append(analysis_tag)
        with atomic():
            analysis.save()
            ProblemAnalysisTag.objects.bulk_create(analysis_tags)

    def _kwargs_filtering(self,
                          filter_function,
                          problem: models.ProblemDAO = None,
                          **kwargs) -> ProblemAnalysisQuerySet:
        if problem is not None:
            assert isinstance(problem, models.ProblemDAO)
            kwargs[ProblemAnalysis.field_name.PROBLEM] = problem
        return filter_function(**kwargs)


class ProblemAnalysisManager(Manager):
    def get_queryset(self) -> ProblemAnalysisQuerySet:
        return ProblemAnalysisQuerySet(self.model, using=self._db)

    def analyze(self, problem: models.ProblemDAO) -> ProblemAnalysis:
        return self.get_queryset().get_by_problem(problem)


class ProblemAnalysis(models.ProblemAnalysisDAO):
    objects: ProblemAnalysisQuerySet
    objects = Manager.from_queryset(ProblemAnalysisQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.ProblemAnalysisDTO:
        return dto.ProblemAnalysisDTO(
            problem_id=self.problem.pk,
            is_analyzed=True,
            time_complexity=self.time_complexity,
            difficulty=self.as_difficulty_dto(),
            hints=self.hints if type(self.hints) is list else [self.hints],
            tags=self.tags(),
        )

    def as_difficulty_dto(self) -> dto.ProblemDifficultyDTO:
        return dto.ProblemDifficultyDTO(enums.ProblemDifficulty(super().difficulty))

    def tags(self) -> List[dto.BOJTagDTO]:
        return [obj.as_dto() for obj in ProblemAnalysisTag.objects.filter(analysis=self)]


class ProblemAnalysisTagQuerySet(QuerySet):
    def exclude(self,
                problem: models.ProblemDAO = None,
                analysis: ProblemAnalysis = None,
                *args,
                **kwargs) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self._kwargs_filtering(super().exclude, problem, analysis, *args, **kwargs)

    def filter(self,
               problem: models.ProblemDAO = None,
               analysis: ProblemAnalysis = None,
               *args,
               **kwargs) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self._kwargs_filtering(super().filter, problem, analysis, *args, **kwargs)

    def problem(self, problem: models.ProblemDAO) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self.filter(problem=problem)

    def analysis(self, analysis: ProblemAnalysis) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self.filter(analysis=analysis)

    def _kwargs_filtering(self,
                          filter_function,
                          problem: models.ProblemDAO = None,
                          analysis: ProblemAnalysis = None,
                          **kwargs) -> ProblemAnalysisQuerySet:
        if problem is not None:
            assert isinstance(problem, models.ProblemDAO)
            try:
                analysis = ProblemAnalysis.objects.problem(problem).latest()
            except ProblemAnalysis.DoesNotExist:
                analysis = ProblemAnalysisTag.objects.none()
            finally:
                kwargs[ProblemAnalysisTag.field_name.ANALYSIS] = analysis
        if analysis is not None:
            assert isinstance(analysis, ProblemAnalysis)
            kwargs[ProblemAnalysisTag.field_name.ANALYSIS] = analysis
        return filter_function(**kwargs)


class ProblemAnalysisTag(models.ProblemAnalysisTagDAO):
    objects: ProblemAnalysisTagQuerySet
    objects = Manager.from_queryset(ProblemAnalysisTagQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.BOJTagDTO:
        return BOJTag.as_dto(self.tag)
