from problems.services.analysers.base import ProblemAnalyzer
from problems.services.analysers.gemini import GeminiProblemAnalyzer


def get_analyzer() -> ProblemAnalyzer:
    return GeminiProblemAnalyzer.get_instance()
