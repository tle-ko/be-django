from problems.models import (
    ProblemDTO,
    ProblemAnalysisDTO,
)


class ProblemAnalyser:
    """문제를 분석하는 클래스의 추상 클래스입니다.

    문제 데이터를 받아와 문제의 분석 결과를 반환하는 analyze() 메소드를 구현해야 합니다.
    """

    def analyze(self, problem: ProblemDTO) -> ProblemAnalysisDTO:
        raise NotImplementedError
