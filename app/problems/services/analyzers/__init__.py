from problems.services.analyzers.base import ProblemAnalyzer
from problems.services.analyzers.gemini import GeminiProblemAnalyzer


def get_analyzer() -> ProblemAnalyzer:
    return GeminiProblemAnalyzer.get_instance()
