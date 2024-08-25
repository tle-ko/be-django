from problems import dto
from problems.services.analysers.base import ProblemAnalyzer


class GPTProblemAnalyzer(ProblemAnalyzer):
    _instance = None

    @classmethod
    def get_instance(cls) -> ProblemAnalyzer:
        if cls._instance is None:
            cls._instance = GPTProblemAnalyzer()
        return cls._instance

    def analyze(self, problem: dto.ProblemDTO) -> dto.ProblemAnalysisDTO:
        raise NotImplementedError
