from typing import Iterable

from apps.problems.models import Problem
from apps.problems.analyses.enums import ProblemDifficulty
from apps.problems.analyses.models import ProblemAnalysis
from apps.problems.analyses.models import ProblemAnalysisTag
from apps.problems.dto import ProblemStatisticDTO


def create_statistics(problems: Iterable[Problem]) -> ProblemStatisticDTO:
    stat = ProblemStatisticDTO()
    for problem in problems:
        stat.sample_count += 1
        try:
            analysis = ProblemAnalysis.objects.get_by_problem(problem)
        except ProblemAnalysis.DoesNotExist:
            stat.difficulty[ProblemDifficulty.UNDER_ANALYSIS] += 1
        else:
            stat.difficulty[ProblemDifficulty(analysis.difficulty)] += 1
            for analysis_tag in ProblemAnalysisTag.objects.analysis(analysis).select_related(ProblemAnalysisTag.field_name.TAG):
                stat.tags[analysis_tag.tag.as_dto()] += 1
    return stat
