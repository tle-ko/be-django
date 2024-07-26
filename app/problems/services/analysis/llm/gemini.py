from problems.services.analysis.analyser import (
    ProblemAnalyser,
    ProblemDTO,
    ProblemAnalysisDTO,
)


class GeminiProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
