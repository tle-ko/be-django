from textwrap import dedent

from apps.analyses.analyzers.base import ProblemDTO
from apps.analyses.analyzers.base import ProblemAnalysisDTO


def get_difficulty_prompt(problem_dto: ProblemDTO, analysis_dto: ProblemAnalysisDTO) -> str:
    sys_msg = dedent("""
        You are a helpful, respectful and honest assistant. Always answer clearly as possible.
        First line of your answer must be one of these words "EASY", "NORMAL", "HARD".
        From 3rd lines, you can reason why you have chosen the difficulty.

        Your goal is to classify the difficulty of user given problem when it is solved in most efficient way.

        Here is how you determine the difficulties.

        "EASY": For beginners in programming, it's not difficult if you have a basic level of computational thinking and understand programming syntax. May require cultivating a bit more logical thinking to solve. Problems which should be tagged as string, implementation, sorting, hash, greedy, binary search, graph, and queue should be considered "EASY".

        "NORMAL": Advanced level for intermediate programmers. Tend to require a more advanced approach to solve. Algorithms, Hashing, Dynamic Programming, Mathematical reasoning, Graph Traversal, and so on...

        "HARD": Highly challenging level for advanced programmers. If you know special algorithms regardless of practical skills, give it a try. These problems are suitable for high-level programming competitions, requiring proficiency and speed. Dynamic Programming, Binary Search, Segment Tree, Priority Queue, ...
    """)
    usr_msg = get_problem_message(problem_dto)
    return build_prompt(sys_msg, usr_msg)


def get_tags_prompt(problem_dto: ProblemDTO, analysis_dto: ProblemAnalysisDTO) -> str:
    sys_msg = dedent("""
        You are a helpful, respectful and honest assistant. Always answer clearly as possible.
        You must answer in English.

        Please ensure that your responses are academically accurate.
        You must not explain details but only answer the tags.

        I will give you some algorithm or data structure tags separated by lines.
        You must only give the algorithmic tag analysis listed in Solved.ac.
        Your goal is to select multiple tags (separated by commas) of the algorithm or data structure below that can best describe the user given problem.
        Please analyze the tags accurately.

        Tags cannot appear at all in tag analysis. You must classify accurately, and these tags must be those listed in solved.ac.
        Make sure that accurate tags are output, not filtered values.
        And if there are multiple tags, be sure to print them all.
    """)
    usr_msg = get_problem_message(problem_dto)
    return build_prompt(sys_msg, usr_msg)


def get_time_complexity_prompt(problem_dto: ProblemDTO, analysis_dto: ProblemAnalysisDTO) -> str:
    sys_msg = dedent("""
        You are a helpful, respectful and honest time-complexity analyst. Always answer clearly as possible.
        Analysts don't converse in natural language as people do. They communicate using intricate equations and symbols, typically preferring the syntax of the LaTeX language.
        Please ensure that your responses are academically accurate.
        Your goal is to find out the short answer about Big-O notated time complexity that can best describe user given problem.

        This is important:
        The first line of your answer must be a single LaTeX syntax wrapped by `$` marks, which is the Big-O notated time complexity.
        Starting from the third lines, you can shortly brief how you have approached to the answer.
    """)
    usr_msg = get_problem_message(problem_dto)
    return build_prompt(sys_msg, usr_msg)


def get_hints_prompt(problem_dto: ProblemDTO, analysis_dto: ProblemAnalysisDTO) -> str:
    assert analysis_dto.tags is not None
    assert analysis_dto.difficulty is not None
    assert analysis_dto.time_complexity is not None
    sys_msg = dedent("""
        You are a helpful, respectful, and honest assistant. Always answer as clearly as possible.
        Please ensure that your responses are academically accurate.
        Your goal is to provide step-by-step hints to help the user solve the given problem.

        I will give you a problem statement, including tags, difficulty, and time complexity.
        Your task is to provide a series of hints to approach and solve the problem. Code should never be included when outputting hints. Your response should be in Korean.
    """)
    usr_msg = dedent(f"""
        Problem Statement:
        {problem_dto.description}

        Tags: {', '.join(analysis_dto.tags)}
        Difficulty: {analysis_dto.difficulty}
        Time Complexity: {analysis_dto.time_complexity}
    """)
    return build_prompt(sys_msg, usr_msg)


def get_problem_message(problem_dto: ProblemDTO) -> str:
    return dedent(f"""
        제목
        {problem_dto.title}

        메모리 제한
        {problem_dto.memory_limit} MB

        시간 제한
        {problem_dto.time_limit} 초

        문제
        {problem_dto.description}

        입력
        {problem_dto.input_description}

        출력
        {problem_dto.output_description}
    """)


def build_prompt(sys_msg: str, usr_msg: str) -> str:
    return dedent(f"""
        <sys> {sys_msg} <sys>
        <usr> {usr_msg} <usr>
    """)
