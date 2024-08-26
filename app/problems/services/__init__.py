from django.db.models import QuerySet

from problems import dto
from problems import models
from problems.services.base import ProblemService
from problems.services.concrete import ConcreteProblemService


def get_problem_service(problem: models.Problem) -> ProblemService:
    return ConcreteProblemService(problem)


def get_problems_statistics(queryset: QuerySet[models.Problem]) -> dto.ProblemStatisticDTO:
    stat = dto.ProblemStatisticDTO()
    for problem in queryset:
        service = get_problem_service(problem)
        for tag in service.query_tags():
            stat.tags[dto.ProblemTagDTO.from_model(tag)] += 1
        stat.difficulty[service.difficulty()] += 1
        stat.sample_count += 1
    return stat
