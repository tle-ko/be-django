from tle.services.analysis import *


class GeminiProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
