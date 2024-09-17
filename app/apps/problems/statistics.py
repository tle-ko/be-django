from collections import Counter
from typing import Iterable

from apps.analyses.enums import ProblemDifficulty
from apps.analyses.models import ProblemAnalysis
from apps.analyses.models import ProblemAnalysisTag

from . import dto
from . import models


def create_statistics(problems: Iterable[models.Problem]) -> dto.ProblemStatisticDTO:
    sample_count = 0
    difficulty_count = Counter()
    tag_count = Counter()
    for problem in problems:
        sample_count += 1
        try:
            analysis = ProblemAnalysis.objects.get_by_problem(problem)
        except ProblemAnalysis.DoesNotExist:
            difficulty = ProblemDifficulty.UNDER_ANALYSIS
            tags = []
        else:
            difficulty = ProblemDifficulty(analysis.difficulty)
            tags = [
                obj.tag.as_dto()
                for obj in ProblemAnalysisTag.objects.analysis(analysis).select_related(ProblemAnalysisTag.field_name.TAG)
            ]
        finally:
            difficulty_count[difficulty] += 1
            for tag_dto in tags:
                tag_count[tag_dto] += 1
    try:
        ratio_denominator = 1 / sample_count
    except ZeroDivisionError:
        ratio_denominator = 0
    finally:
        return dto.ProblemStatisticDTO(
            sample_count=sample_count,
            difficulty=[
                dto.ProblemDifficultyStaticDTO(
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
