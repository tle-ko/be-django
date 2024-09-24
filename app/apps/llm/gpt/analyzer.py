from .. import base


class GPTProblemAnalyzer(base.ProblemAnalyzer):
    _instance = None

    @classmethod
    def get_instance(cls) -> base.ProblemAnalyzer:
        if cls._instance is None:
            cls._instance = GPTProblemAnalyzer()
        return cls._instance

    def analyze(self, problem: base.ProblemDetailDTO) -> base.ProblemAnalysisRawDTO:
        raise NotImplementedError
