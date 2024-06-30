from __future__ import annotations

from .models import ProblemDTO, AnalysisDTO


def get_analyser() -> ProblemAnalyser:
    return GPTProblemAnalyser()


class ProblemAnalyser:
    def analyze(self, problem: ProblemDTO) -> AnalysisDTO:
        raise NotImplementedError


class GPTProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> AnalysisDTO:
        raise NotImplementedError


class GeminiProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> AnalysisDTO:
        raise NotImplementedError
