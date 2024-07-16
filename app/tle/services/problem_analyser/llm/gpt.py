from tle.services.problem_analyser import *


class GPTProblemAnalyser(ProblemAnalyser):
    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
