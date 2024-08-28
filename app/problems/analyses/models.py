from __future__ import annotations

from typing import Union

from django.db import models
from django.db.transaction import atomic

from problems.analyses.dto import ProblemAnalysisDTO
from problems.analyses.dto import ProblemTagDTO
from problems.analyses.enums import ProblemDifficulty
from problems.models import Problem


class ProblemTagManager(models.Manager):
    def get_by_key(self, key: str) -> ProblemTag:
        return self.get(**{ProblemTag.field_name.KEY: key})


class ProblemTag(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 키를 입력해주세요. (최대 20자)',
    )
    name_ko = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(국문)을 입력해주세요. (최대 50자)',
    )
    name_en = models.CharField(
        max_length=50,
        unique=True,
        help_text='알고리즘 태그 이름(영문)을 입력해주세요. (최대 50자)',
    )

    objects: _ProblemTagManager = ProblemTagManager()

    class field_name:
        KEY = 'key'
        NAME_KO = 'name_ko'
        NAME_EN = 'name_en'

    class Meta:
        ordering = ['key']

    def __repr__(self) -> str:
        return f'[#{self.key}]'

    def __str__(self) -> str:
        return f'{self.pk} : {self.__repr__()} ({self.name_ko})'

    def as_dto(self) -> ProblemTagDTO:
        return ProblemTagDTO(
            key=self.key,
            name_ko=self.name_ko,
            name_en=self.name_en,
        )


class ProblemTagRelation(models.Model):
    parent = models.ForeignKey(
        ProblemTag,
        on_delete=models.CASCADE,
        related_name='parent'
    )
    child = models.ForeignKey(
        ProblemTag,
        on_delete=models.CASCADE,
        related_name='child'
    )

    class field_name:
        PARENT = 'parent'
        CHILD = 'child'

    def __str__(self) -> str:
        return f'{self.pk} : #{self.parent.key} <- #{self.child.key}'


class ProblemAnalysisManager(models.Manager):
    def problem(self, problem: Problem) -> _ProblemAnalysisManager:
        return self.filter(**{ProblemAnalysis.field_name.PROBLEM: problem})

    def get_by_problem(self, problem: Problem) -> ProblemAnalysis:
        return self.problem(problem).latest()

    def create_from_dto(self, analysis_dto: ProblemAnalysisDTO) -> ProblemAnalysis:
        analysis = ProblemAnalysis(**{
            ProblemAnalysis.field_name.PROBLEM: analysis_dto.problem_id,
            ProblemAnalysis.field_name.TIME_COMPLEXITY: analysis_dto.time_complexity,
            ProblemAnalysis.field_name.DIFFICULTY: ProblemDifficulty.from_label(analysis_dto.difficulty),
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


class ProblemAnalysis(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text='문제를 입력해주세요.',
    )
    difficulty = models.IntegerField(
        help_text='문제 난이도를 입력해주세요.',
        choices=ProblemDifficulty.choices,
    )
    time_complexity = models.CharField(
        max_length=100,
        help_text=(
            '문제 시간 복잡도를 입력해주세요. ',
            '예) O(1), O(n), O(n^2), O(V \log E) 등',
        ),
        validators=[
            # TODO: 시간 복잡도 검증 로직 추가
        ],
    )
    hint = models.JSONField(
        help_text='문제 힌트를 입력해주세요. Step-by-step 으로 입력해주세요.',
        validators=[
            # TODO: 힌트 검증 로직 추가
        ],
        blank=False,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects: _ProblemAnalysisManager = ProblemAnalysisManager()

    class field_name:
        PROBLEM = 'problem'
        DIFFICULTY = 'difficulty'
        TAGS = 'tags'
        TIME_COMPLEXITY = 'time_complexity'
        HINT = 'hint'
        CREATED_AT = 'created_at'

    class Meta:
        verbose_name_plural = 'Problem analyses'
        ordering = ['-created_at']
        get_latest_by = ['created_at']

    def __str__(self):
        return f'[Analyse of {self.problem}]'


class ProblemAnalysisTagManager(models.Manager):
    def problem(self, problem: Problem) -> _ProblemAnalysisTagManager:
        try:
            analysis = ProblemAnalysis.objects.get_by_problem(problem)
        except ProblemAnalysis.DoesNotExist:
            return ProblemAnalysisTag.objects.none()
        else:
            return self.analysis(analysis)

    def analysis(self, analysis: ProblemAnalysis) -> _ProblemAnalysisTagManager:
        return self.filter(**{ProblemAnalysisTag.field_name.ANALYSIS: analysis})


class ProblemAnalysisTag(models.Model):
    analysis = models.ForeignKey(
        ProblemAnalysis,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    tag = models.ForeignKey(
        ProblemTag,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        help_text='문제의 DSA 태그를 입력해주세요.',
    )

    objects: _ProblemAnalysisTagManager = ProblemAnalysisTagManager()

    class field_name:
        ANALYSIS = 'analysis'
        TAG = 'tag'

    def __str__(self):
        return f'{self.analysis.problem} #{self.tag}'


_ProblemTagManager = Union[ProblemTagManager, models.Manager[ProblemTag]]
_ProblemAnalysisManager = Union[ProblemAnalysisManager,
                                models.Manager[ProblemAnalysis]]
_ProblemAnalysisTagManager = Union[ProblemAnalysisTagManager,
                                   models.Manager[ProblemAnalysisTag]]
