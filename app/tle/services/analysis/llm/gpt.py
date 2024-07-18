from tle.services.analysis import *


class GPTProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
