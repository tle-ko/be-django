from tle.services.problem_analyser import *


class GeminiProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
