from collections import Counter
from typing import Iterable

from . import dto
from . import enums
from . import proxy


def create_statistics(problems: Iterable[proxy.Problem]) -> dto.ProblemStatisticDTO:
    problem_count = 0
    difficulty_count = Counter()
    tag_count = Counter()
    for problem in problems:
        problem_count += 1
        try:
            analysis = proxy.ProblemAnalysis.objects.get_by_problem(problem)
        except proxy.ProblemAnalysis.DoesNotExist:
            difficulty = enums.ProblemDifficulty.UNDER_ANALYSIS
            tags = []
        else:
            difficulty = enums.ProblemDifficulty(analysis.difficulty)
            tags = [
                obj.as_dto()
                for obj in proxy.ProblemAnalysisTag.objects.analysis(analysis).select_related(proxy.ProblemAnalysisTag.field_name.TAG)
            ]
        difficulty_count[difficulty] += 1
        for tag_dto in tags:
            tag_count[tag_dto] += 1
    try:
        ratio_denominator = 1 / problem_count
    except ZeroDivisionError:
        ratio_denominator = 0
    finally:
        return dto.ProblemStatisticDTO(
            problem_count=problem_count,
            difficulties=[
                dto.enums.ProblemDifficultyStaticDTO(
                    difficulty=difficulty,
                    count=count,
                    ratio=count*ratio_denominator,
                )
                for difficulty, count in difficulty_count.items()
            ],
            tags=[
                dto.ProblemTagStaticDTO(
                    tag=tag,
                    count=count,
                    ratio=count*ratio_denominator,
                )
                for tag, count in tag_count.items()
            ],
        )
