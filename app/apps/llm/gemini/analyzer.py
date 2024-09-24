from logging import getLogger

from django.conf import settings
from google import generativeai as genai

from .. import base
from . import parsers
from . import prompts


logger = getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiProblemAnalyzer(base.ProblemAnalyzer):
    _instance = None

    @classmethod
    def get_instance(cls) -> base.ProblemAnalyzer:
        if cls._instance is None:
            cls._instance = GeminiProblemAnalyzer()
        return cls._instance

    def __init__(self) -> None:
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

    def analyze(self, problem_dto: base.ProblemDetailDTO) -> base.ProblemAnalysisRawDTO:
        assert isinstance(problem_dto, base.ProblemDetailDTO)
        analysis_dto = base.ProblemAnalysisRawDTO(
            problem_id=problem_dto.problem_id,
            difficulty=None,
            time_complexity=None,
            tags=None,
            hints=None,
        )

        logger.info(f'"{problem_dto.title}" 문제의 분석 시작.')
        chat = self.model.start_chat(history=[])

        logger.info(f'... 태그 분석 중...')
        logger.info(f'... 태그 프롬프트 생성 중...')
        prompt = prompts.get_tags_prompt(problem_dto, analysis_dto)
        logger.info(f'... 태그 프롬프트 질의 중...')
        response = chat.send_message(content=prompt)
        logger.info(f'... 태그 프롬프트 질의 답변 수신 완료...')
        assistant_message = response.text
        logger.info(f'... 태그 프롬프트 파싱 중...')
        analysis_dto.tags = parsers.parse_tags(assistant_message)

        logger.info(f'... 난이도 분석 중...')
        prompt = prompts.get_difficulty_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.difficulty = parsers.parse_difficulty(assistant_message)

        logger.info(f'... 시간 복잡도 분석 중...')
        prompt = prompts.get_time_complexity_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.time_complexity = parsers.parse_time_complexity(assistant_message)

        logger.info(f'... 힌트 분석 중...')
        prompt = prompts.get_hints_prompt(problem_dto, analysis_dto)
        assistant_message = chat.send_message(content=prompt).text
        analysis_dto.hints = parsers.parse_hints(assistant_message)

        logger.info(f'"{problem_dto.title}" 문제의 분석 완료.')
        return analysis_dto
