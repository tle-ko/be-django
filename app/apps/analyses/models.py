from __future__ import annotations

from typing import Any
from typing import List
from typing import Union

from django.db.models import Manager
from django.db.models import QuerySet
from django.db.transaction import atomic

from apps.problems.models import Problem

from . import db
from . import dto


class ProblemTagQuerySet(QuerySet):
    def get_by_key(self, key: str) -> ProblemTag:
        return self.get(**{ProblemTag.field_name.KEY: key})


class ProblemTag(db.ProblemTagDAO):
    objects: ProblemTagQuerySet
    objects = Manager.from_queryset(ProblemTagQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.ProblemTagDTO:
        return dto.ProblemTagDTO(
            key=self.key,
            name_ko=self.name_ko,
            name_en=self.name_en,
        )


class ProblemTagRelation(db.ProblemTagRelationDAO):
    class Meta:
        proxy = True


class ProblemAnalysisQuerySet(QuerySet):
    def exclude(self,
                problem: Problem = None,
                *args: Any,
                **kwargs: Any) -> ProblemAnalysisQuerySet:
        return self._kwargs_filtering(super().exclude, problem, *args, **kwargs)

    def filter(self,
               problem: Problem = None,
               *args: Any,
               **kwargs: Any) -> ProblemAnalysisQuerySet:
        return self._kwargs_filtering(super().filter, problem, *args, **kwargs)

    def get_by_problem(self, problem: Problem) -> ProblemAnalysis:
        return self.problem(problem).latest()

    def problem(self, problem: Problem) -> ProblemAnalysisQuerySet:
        return self.filter(problem=problem)

    def create_from_dto(self, analysis_dto: dto.ProblemAnalysisRawDTO) -> ProblemAnalysis:
        analysis = ProblemAnalysis(**{
            ProblemAnalysis.field_name.PROBLEM: analysis_dto.problem_id,
            ProblemAnalysis.field_name.TIME_COMPLEXITY: analysis_dto.time_complexity,
            ProblemAnalysis.field_name.DIFFICULTY: analysis_dto.difficulty,
            ProblemAnalysis.field_name.HINT: analysis_dto.hints,
        })
        analysis_tags = []
        for tag_key in analysis_dto.tags:
            tag = ProblemTag.objects.get_by_key(tag_key)
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
                          problem: Problem = None,
                          **kwargs) -> ProblemAnalysisQuerySet:
        if problem is not None:
            assert isinstance(problem, Problem)
            kwargs[ProblemAnalysis.field_name.PROBLEM] = problem
        return filter_function(**kwargs)


class ProblemAnalysis(db.ProblemAnalysisDAO):
    objects: ProblemAnalysisQuerySet
    objects = Manager.from_queryset(ProblemAnalysisQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.ProblemAnalysisDTO:
        return dto.ProblemAnalysisDTO(
            problem_id=self.problem.pk,
            is_analyzed=True,
            time_complexity=self.time_complexity,
            difficulty=self.difficulty,
            hints=self.hint,
            tags=self.tags.all().as_dto(),
        )

    def tags(self) -> List[dto.ProblemTagDTO]:
        return [obj.as_dto() for obj in ProblemAnalysisTag.objects.filter(analysis=self)]


class ProblemAnalysisTagQuerySet(QuerySet):
    def exclude(self,
                problem: Problem = None,
                analysis: ProblemAnalysis = None,
                *args: Any,
                **kwargs: Any) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self._kwargs_filtering(super().exclude, problem, analysis, *args, **kwargs)

    def filter(self,
               problem: Problem = None,
               analysis: ProblemAnalysis = None,
               *args: Any,
               **kwargs: Any) -> Union[ProblemAnalysisTagQuerySet, QuerySet[ProblemAnalysisTag]]:
        return self._kwargs_filtering(super().filter, problem, analysis, *args, **kwargs)

    def problem(self, problem: Problem) -> ProblemAnalysisTagQuerySet:
        return self.filter(problem=problem)

    def analysis(self, analysis: ProblemAnalysis) -> ProblemAnalysisTagQuerySet:
        return self.filter(analysis=analysis)

    def _kwargs_filtering(self,
                          filter_function,
                          problem: Problem = None,
                          analysis: ProblemAnalysis = None,
                          **kwargs) -> ProblemAnalysisQuerySet:
        if problem is not None:
            assert isinstance(problem, Problem)
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


class ProblemAnalysisTag(db.ProblemAnalysisTagDAO):
    objects: ProblemAnalysisTagQuerySet
    objects = Manager.from_queryset(ProblemAnalysisTagQuerySet)()

    class Meta:
        proxy = True

    def as_dto(self) -> dto.ProblemTagDTO:
        return ProblemTag.as_dto(self.tag)
