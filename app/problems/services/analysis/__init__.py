from __future__ import annotations

from problems.models import Problem, ProblemAnalysis, ProblemDTO
from problems.services.analysis.analyser import ProblemAnalyser
from problems.services.analysis.llm.gemini import GeminiProblemAnalyser


__all__ = (
    'ProblemAnalyser',
    'get_analyser',
)


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

    def analyze(self, problem: Problem) -> ProblemAnalysis:
        problem_dto = ProblemDTO(
            title=problem.title,
            description=problem.description,
            input_description=problem.input_description,
            output_description=problem.output_description,
            memory_limit_megabyte=problem.memory_limit_megabyte,
            time_limit_second=problem.time_limit_second,
        )
        analyzer = self.get_analyzer()
        analysis_dto = analyzer.analyze(problem_dto)
        return ProblemAnalysis(**{
            ProblemAnalysis.field_name.PROBLEM: problem,
            ProblemAnalysis.field_name.DIFFICULTY: analysis_dto.difficulty,
            ProblemAnalysis.field_name.TAGS: analysis_dto.tags,
            ProblemAnalysis.field_name.TIME_COMPLEXITY: analysis_dto.time_complexity,
            ProblemAnalysis.field_name.HINT: analysis_dto.hint,
        })
