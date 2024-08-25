from __future__ import annotations

from typing import List
from typing import Optional

from django.db.models import QuerySet

from problems import enums
from problems import models


class ProblemService:
    def __init__(self, instance: models.Problem) -> None:
        assert isinstance(instance, models.Problem)
        self.instance = instance

    def query_analyses(self) -> QuerySet[models.ProblemAnalysis]:
        raise NotImplementedError

    def query_tags(self) -> QuerySet[models.ProblemAnalysisTag]:
        raise NotImplementedError

    def get_analysis(self) -> Optional[models.ProblemAnalysis]:
        """
        raises:
            ProblemAnalysis.DoesNotExists
        """
        raise NotImplementedError

    def is_analyzed(self) -> bool:
        raise NotImplementedError

    def analyze(self) -> None:
        """문제를 분석합니다.

        오래 걸리는 작업인 만큼 본 함수는 분석 작업을 예약만 하고,
        실제 분석은 비동기적으로 진행됩니다."""
        raise NotImplementedError

    def difficulty(self) -> enums.ProblemDifficulty:
        raise NotImplementedError

    def time_complexity(self) -> str:
        raise NotImplementedError

    def tags(self) -> List[str]:
        raise NotImplementedError

    def hints(self) -> List[str]:
        raise NotImplementedError
