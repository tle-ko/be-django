from functools import cache
from logging import getLogger
from typing import List
import re

from sympy import latex
from sympy.parsing.latex import parse_latex

from apps.analyses.models import ProblemTag


logger = getLogger(__name__)


@cache
def get_valid_tags() -> List[str]:
    """실제로 존재하는 태그의 목록을 가져온다. (solved.ac 태그 기준)

    비싼 연산이므로 캐시하여 사용한다.
    """
    return [*ProblemTag.objects.values_list(ProblemTag.field_name.KEY, flat=True)]


def parse_difficulty(assistant_message: str) -> str:
    return assistant_message.strip().split('\n')[0]


def parse_tags(assistant_message: str) -> List[str]:
    tags = []
    # 1. 실제로 존재하는 태그의 목록을 가져온다. (solved.ac 태그 기준)
    valid_tags = get_valid_tags()
    # 2.
    tokens = assistant_message.split(',')
    logger.info(f'ANALYSER TAG {len(tokens)} 개의 후보로 시작. ({", ".join(tokens)})')
    regex = re.compile(r"^[a-zA-Z0-9_]+$")
    for token in tokens:
        token = token.strip().lower().replace(" ", "_")
        if regex.match(token) and (token in valid_tags):
            tags.append(token)
            logger.info(f'... 태그가 선택됨: "{token}"')
        else:
            logger.info(f'... 태그가 선택되지 않음: "{token}"')
    logger.info(f'ANALYSER TAG {len(tags)} 개의 후보로 종료. ({", ".join(tags)})')
    return tags


def parse_time_complexity(assistant_message: str) -> str:
    match = re.search(r"\$O\((.*?)\)\$", assistant_message)
    if match:
        complexity = match.group(1)
        try:
            parsed_expr = parse_latex(complexity)
            latex_str = latex(parsed_expr)
            return f"{latex_str}"
        except Exception as e:
            return f"Invalid LaTeX expression: {str(e)}"
    else:
        return "No complexity found"


def parse_hints(assistant_message: str) -> List[str]:
    return re.sub(r"##.*", "", assistant_message).strip()
