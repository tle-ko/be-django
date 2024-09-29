from apps.submissions.models import SubmissionDAO
from apps.problems.converters import ProblemAnalysisConverter
from common.converters import ModelConverter
from users.models import User

from . import dto
from . import models


class CrewActivityProblemConverter(ModelConverter[models.CrewActivityProblemDAO, dto.CrewActivityProblemDTO]):
    def instance_to_dto(self, instance: models.CrewActivityProblemDAO) -> dto.CrewActivityProblemDTO:
        return dto.CrewActivityProblemDTO(
            problem_id=instance.pk,
            order=instance.order,
            problem_ref_id=instance.problem.pk,
            title=instance.problem.title,
            analysis=ProblemAnalysisConverter().problem_to_dto(instance.problem),
        )


class CrewActivityProblemDetailConverter(ModelConverter[models.CrewActivityProblemDAO, dto.CrewActivityProblemDetailDTO]):
    def __init__(self, user: User) -> None:
        self.user = user

    def instance_to_dto(self, instance: models.CrewActivityProblemDAO) -> dto.CrewActivityProblemDetailDTO:
        obj = dto.CrewActivityProblemDetailDTO(
            problem_id=None,
            problem_ref_id=None,
            order=None,
            title=None,
            analysis=None,
            link=None,
            description=None,
            input_description=None,
            output_description=None,
            memory_limit=None,
            time_limit=None,
            created_at=None,
            submission_id=None,
            has_submitted=None,
        )
        obj.problem_id = instance.pk
        obj.order = instance.order
        self._update_problem_data(instance, obj)
        self._update_submission_data(instance, obj)
        return obj

    def _update_problem_data(self, instance: models.CrewActivityProblemDAO, obj: dto.CrewActivityProblemDetailDTO):
        problem_dto = instance.problem.as_detail_dto()
        obj.analysis = problem_dto.analysis
        obj.problem_ref_id = problem_dto.problem_ref_id
        obj.title = problem_dto.title
        obj.link = problem_dto.link
        obj.description = problem_dto.description
        obj.input_description = problem_dto.input_description
        obj.output_description = problem_dto.output_description
        obj.memory_limit = problem_dto.memory_limit
        obj.time_limit = problem_dto.time_limit
        obj.created_at = problem_dto.created_at

    def _update_submission_data(self, instance: models.CrewActivityProblemDAO, obj: dto.CrewActivityProblemDetailDTO):
        try:
            obj.submission_id = SubmissionDAO.objects.filter(**{
                SubmissionDAO.field_name.USER: self.user,
                SubmissionDAO.field_name.PROBLEM: instance,
            }).latest().pk
            obj.has_submitted = True
        except SubmissionDAO.DoesNotExist:
            obj.has_submitted = False
