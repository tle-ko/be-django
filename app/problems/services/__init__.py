from problems import models
from problems.services.base import ProblemService
from problems.services.concrete import ConcreteProblemService


def get_problem_service(problem: models.Problem) -> ProblemService:
    return ConcreteProblemService(problem)
