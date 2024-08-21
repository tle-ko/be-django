from __future__ import annotations

from typing import List
from typing import Optional

from django.db.models import QuerySet

from problems import models


class ProblemService:
    def __init__(self, instance: models.Problem) -> None:
        assert isinstance(instance, models.Problem)
        self.instance = instance

    def analyses(self) -> QuerySet[models.ProblemAnalysis]:
        return models.ProblemAnalysis.objects.filter(**{
            models.ProblemAnalysis.field_name.PROBLEM: self.instance,
        })

    def analysis(self) -> Optional[models.ProblemAnalysis]:
        if not self.is_analyzed():
            return None
        return self.analyses().latest()

    def is_analyzed(self) -> bool:
        return self.analyses().exists()

    def analyze(self):
        # TODO
        pass


class ProblemAnalysisService:
    @staticmethod
    def from_problem(problem: models.Problem) -> ProblemAnalysisService:
        analysis = ProblemService(problem).analysis()
        return ProblemAnalysisService(analysis)

    def __init__(self, instance: Optional[models.ProblemAnalysis] = None) -> None:
        if instance is None:
            self._strategy = UnanalyzedProblemAnalysisService()
        else:
            self._strategy = AnalyzedProblemAnalysisService(instance)

    def is_analyzed(self) -> bool:
        return self._strategy.is_analyzed()

    def difficulty(self) -> models.ProblemDifficultyChoices:
        return self._strategy.difficulty()

    def difficulty_description(self) -> str:
        return self._strategy.difficulty_description()

    def time_complexity(self) -> str:
        return self._strategy.time_complexity()

    def time_complexity_description(self) -> str:
        return self._strategy.time_complexity_description()

    def tags(self) -> List[models.ProblemTag]:
        return self._strategy.tags()

    def hints(self) -> List[str]:
        return self._strategy.hints()


class UnanalyzedProblemAnalysisService(ProblemAnalysisService):
    def __init__(self, *args, **kwargs) -> None:
        return

    def is_analyzed(self) -> bool:
        return False

    def difficulty(self) -> models.ProblemDifficultyChoices:
        return models.ProblemDifficultyChoices.UNDER_ANALYSIS

    def time_complexity(self) -> str:
        return ''

    def tags(self) -> List[models.ProblemTag]:
        return []

    def hints(self) -> List[str]:
        return []

    def difficulty_description(self) -> str:
        return "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"

    def time_complexity_description(self) -> str:
        return "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"


class AnalyzedProblemAnalysisService(ProblemAnalysisService):
    def __init__(self, instance: models.ProblemAnalysis) -> None:
        assert isinstance(instance, models.ProblemAnalysis)
        self.instance = instance

    def is_analyzed(self) -> bool:
        return True

    def difficulty(self) -> models.ProblemDifficultyChoices:
        return models.ProblemDifficultyChoices(self.instance.difficulty)

    def time_complexity(self) -> str:
        return self.instance.time_complexity

    def tags(self) -> List[models.ProblemTag]:
        return models.ProblemAnalysisTag.objects.filter(**{
            models.ProblemAnalysisTag.field_name.ANALYSIS: self.instance,
        }).values_list(models.ProblemAnalysisTag.field_name.TAG, flat=True)

    def hints(self) -> List[str]:
        return self.instance.hint

    def difficulty_description(self) -> str:
        return "기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준 [이 기능은 추가될 예정이 없습니다]"

    def time_complexity_description(self) -> str:
        return "선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요. [이 기능은 추가될 예정이 없습니다]"
