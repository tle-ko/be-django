from __future__ import annotations

from problems import dto
from problems.services.analysis.analyser import ProblemAnalyser
from problems.services.analysis.llm.gemini import GeminiProblemAnalyser



class AnalysingService:
    instance = None
    analyzer_class = GeminiProblemAnalyser

    @classmethod
    def get_instance(cls) -> AnalysingService:
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def get_analyzer(self) -> ProblemAnalyser:
        return self.analyzer_class()

    def analyze(self, problem: dto.ProblemDTO) -> dto.ProblemAnalysisDTO:
        analyzer = self.get_analyzer()
        return analyzer.analyze(problem)
