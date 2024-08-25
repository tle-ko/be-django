from logging import getLogger

from django.conf import settings
from google import generativeai as genai

from problems.dto import ProblemDTO
from problems.dto import ProblemAnalysisDTO
from problems.services.analysers.base import ProblemAnalyzer
from problems.services.analysers.gemini import prompts
from problems.services.analysers.gemini import parsers


# TODO: replace log channel
logger = getLogger('django.server')


class GeminiProblemAnalyzer(ProblemAnalyzer):
    _instance = None

    @classmethod
    def get_instance(cls) -> ProblemAnalyzer:
        if cls._instance is None:
            cls._instance = GeminiProblemAnalyzer()
        return cls._instance

    def __init__(self) -> None:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )

    def analyze(self, problem_dto: ProblemDTO) -> ProblemAnalysisDTO:
        chat = self.model.start_chat(history=[])

        analysis_dto = ProblemAnalysisDTO(
            difficulty=None,
            time_complexity=None,
            tags=None,
            hints=None,
        )

        prompt = prompts.get_tags_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.tags = parsers.parse_tags(assistant_message)

        prompt = prompts.get_difficulty_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.difficulty = parsers.parse_difficulty(assistant_message)

        prompt = prompts.get_time_complexity_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.time_complexity = parsers.parse_time_complexity(
            assistant_message)

        prompt = prompts.get_hints_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.hints = parsers.parse_hints(assistant_message)

        return analysis_dto
