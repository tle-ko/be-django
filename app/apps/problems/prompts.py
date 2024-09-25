from functools import lru_cache
from textwrap import dedent
import typing
import re

from sympy import latex
from sympy.parsing.latex import parse_latex

from apps.boj.proxy import BOJTag

from . import models


@lru_cache
def valid_tags() -> typing.List[str]:
    """허용되는 태그의 목록을 가져온다."""
    return BOJTag.objects.values_list(BOJTag.field_name.KEY, flat=True)


class PromptHandler:
    def create_propmt(self, problem: models.ProblemDAO, context: dict = {}) -> str:
        raise NotImplementedError

    def parse_response(self, response: str):
        raise NotImplementedError


# PromptHandler를 상속받아 작성하면 된다.


class TagPromptHandler(PromptHandler):
    def create_propmt(self, problem: models.ProblemDAO, context: dict = {}) -> str:
        return dedent(f"""
            <sys>
            You are a helpful, respectful, and honest assistant. Always respond as clearly and concisely as possible in English.

            Your task is to analyze the given algorithm or data structure tags and return only the relevant tags from the Solved.ac platform.
            Ensure the tags come directly from the Solved.ac list.
            Respond with multiple tags (separated by commas) that best describe the problem.
            Do not provide any explanations. Only output the selected tags.
            Reference: https://solved.ac/api/v3/tag/list
            <sys>
            <usr>
            제목
            {problem.title}

            메모리 제한
            {problem.memory_limit} MB

            시간 제한
            {problem.time_limit} 초

            문제
            {problem.description}

            입력
            {problem.input_description}

            출력
            {problem.output_description}
            <usr>
        """)

    def parse_response(self, response: str) -> typing.List[str]:
        tags = []
        raw_tokens = response.split(',')
        for raw_token in raw_tokens:
            token = raw_token.strip().replace(" ", "_").lower()
            if not re.match(r"^[a-zA-Z0-9_]+$", token):
                continue
            if token not in valid_tags():
                continue
            tags.append(token)
        return tags


class TimeComplexityPromptHandler(PromptHandler):
    def create_propmt(self, problem: models.ProblemDAO, context: dict = {}) -> str:
        return dedent(f"""
            <sys>
            You are a helpful, respectful and honest time-complexity analyst. Always answer clearly as possible.
            Analysts don't converse in natural language as people do. They communicate using intricate equations and symbols, typically preferring the syntax of the LaTeX language.
            Please ensure that your responses are academically accurate.
            Your goal is to find out the short answer about Big-O notated time complexity that can best describe user given problem.

            This is important:
            The first line of your answer must be a single LaTeX syntax wrapped by `$` marks, which is the Big-O notated time complexity.
            Starting from the third lines, you can shortly brief how you have approached to the answer.
            <sys>
            <usr>
            제목
            {problem.title}

            메모리 제한
            {problem.memory_limit} MB

            시간 제한
            {problem.time_limit} 초

            문제
            {problem.description}

            입력
            {problem.input_description}

            출력
            {problem.output_description}
            <usr>
        """)

    def parse_response(self, response: str) -> str:
        match = re.search(r"\$O\((.*?)\)\$", response)
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


class DifficultyPromptHandler(PromptHandler):
    def create_propmt(self, problem: models.ProblemDAO, context: dict = {}) -> str:
        return dedent(f"""
            <sys>
            You are a helpful, respectful and honest assistant. Always answer clearly as possible.
            First line of your answer must be one of these words "EASY", "NORMAL", "HARD".
            From 3rd lines, you can reason why you have chosen the difficulty.

            Your goal is to classify the difficulty of user given problem when it is solved in most efficient way.

            Here is how you determine the difficulties.

            "EASY": For beginners in programming, it's not difficult if you have a basic level of computational thinking and understand programming syntax. May require cultivating a bit more logical thinking to solve. Problems which should be tagged as string, implementation, sorting, hash, greedy, binary search, graph, and queue should be considered "EASY".

            "NORMAL": Advanced level for intermediate programmers. Tend to require a more advanced approach to solve. Algorithms, Hashing, Dynamic Programming, Mathematical reasoning, Graph Traversal, and so on...

            "HARD": Highly challenging level for advanced programmers. If you know special algorithms regardless of practical skills, give it a try. These problems are suitable for high-level programming competitions, requiring proficiency and speed. Dynamic Programming, Binary Search, Segment Tree, Priority Queue, ...
            <sys>
            <usr>
            제목
            {problem.title}

            메모리 제한
            {problem.memory_limit} MB

            시간 제한
            {problem.time_limit} 초

            문제
            {problem.description}

            입력
            {problem.input_description}

            출력
            {problem.output_description}
            <usr>
        """)

    def parse_response(self, response: str) -> str:
        return response.strip().split('\n')[0]


class HintsPromptHandler(PromptHandler):
    def create_propmt(self, problem: models.ProblemDAO, context: dict = {}) -> str:
        return dedent(f"""
            <sys>
            You are a helpful, respectful, and honest assistant. Always answer as clearly as possible.
            Ensure your responses are academically accurate.
                        
            Your goal is to provide step-by-step hints to help the user solve the given problem, without including any code in your response. The hints must be written in Korean.

            Format the hints as follows:
            1. First step: describe the initial approach.
            2. Second step: describe the next approach, leading towards the solution.
            3. Third step: continue guiding step-by-step toward the solution.

            Each step should begin with a number ("1.", "2.", "3.", etc.), ensuring the hints are clear, concise, and easy for the user to follow. No additional content should be provided beyond these numbered steps.
            <sys>
            <usr>
            Problem Statement:
            제목
            {problem.title}

            메모리 제한
            {problem.memory_limit} MB

            시간 제한
            {problem.time_limit} 초

            문제
            {problem.description}

            입력
            {problem.input_description}

            출력
            {problem.output_description}

            Tags: {', '.join(context['tags'])}
            Difficulty: {context['difficulty']}
            Time Complexity: {context['time_complexity']}
            <usr>
        """)

    def parse_response(self, response: str) -> typing.List[str]:
        return [re.sub(r"##.*", "", response).strip()]
