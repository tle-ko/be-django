from problems import dto
from problems import models


def get_analysis(problem: models.Problem) -> dto.ProblemAnalysisDTO:
    queryset = models.ProblemAnalysis.objects.filter(**{
        models.ProblemAnalysis.field_name.PROBLEM: problem
    })
    try:
        analysis = queryset.latest()
        tag_keys = models.ProblemAnalysisTag.objects.filter(**{
            models.ProblemAnalysisTag.field_name.ANALYSIS: analysis,
        }).values_list(
            models.ProblemAnalysisTag.field_name.TAG+'__'+models.ProblemTag.field_name.KEY,
            flat=True,
        )
    except models.ProblemAnalysis.DoesNotExist:
        return dto.ProblemAnalysisDTO(
            time_complexity='',
            difficulty=models.ProblemDifficultyChoices.UNDER_ANALYSIS,
        )
    else:
        return dto.ProblemAnalysisDTO(
            time_complexity=analysis.time_complexity,
            difficulty=models.ProblemDifficultyChoices(analysis.difficulty),
            hint=tuple(analysis.hint),
            tags=tuple(tag_keys),
        )
