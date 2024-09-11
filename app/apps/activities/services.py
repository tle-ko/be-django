from typing import Dict

from apps.activities import dto
from apps.activities import models
from apps.submissions.models import Submission
from apps.submissions.models import SubmissionComment
from users.models import User


def get_user_submission_table(activity: models.CrewActivity, user: User) -> dto.UserSubmissionTableDTO:
    table: Dict[int, dto.UserSubmissionTableRowDTO] = dict()
    for problem in models.CrewActivityProblem.objects.filter(activity=activity):
        table[problem.order] = dto.UserSubmissionTableRowDTO(
            submission_id=None,
            problem_id=problem.pk,
            problem_title=problem.problem.title,
            problem_order=problem.order,
            reviewers=[],
            created_at=None,
            is_submitted=False,
        )
    for submission in Submission.objects.filter(activity=activity, user=user):
        table[submission.problem.order] = dto.UserSubmissionTableRowDTO(
            submission_id=submission.pk,
            problem_id=submission.problem.pk,
            problem_title=submission.problem.problem.title,
            problem_order=submission.problem.order,
            reviewers={
                review.created_by.pk: dto.UserDTO(
                    user_id=review.created_by.pk,
                    username=review.created_by.username,
                    profile_image=review.created_by.profile_image,
                )
                for review in SubmissionComment.objects.filter(submission=submission)
            }.values(),
            created_at=submission.created_at,
            is_submitted=True,
        )
    return dto.UserSubmissionTableDTO(
        submissions=sorted(table.values(), key=lambda row: row.problem_order),
        submitted_by=dto.UserDTO(
            user_id=user.pk,
            username=user.username,
            profile_image=user.profile_image,
        ),
    )
