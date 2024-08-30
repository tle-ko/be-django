from typing import List

from django.db.models import QuerySet

from boj.enums import BOJLevel
from app.crews.servicesa import dto
from crews import enums
from crews import models
from problems.dto import ProblemStatisticDTO
from problems.models import Problem
from users.models import User


class UserCrewService:
    def __init__(self, instance: User) -> None:
        assert isinstance(instance, User)
        self.instance = instance

    def query_crews_joined(self) -> QuerySet[models.Crew]:
        """자신이 멤버로 있는 크루를 조회하는 쿼리를 반환"""
        ...

    def query_crews_recruiting(self) -> QuerySet[models.Crew]:
        """자신이 멤버로 있지 않으면서 크루원을 모집중인 크루를 조회하는 쿼리를 반환"""
        ...


class CrewService:
    def __init__(self, instance: models.Crew) -> None:
        assert isinstance(instance, models.Crew)
        self.instance = instance

    def query_members(self) -> QuerySet[models.CrewMember]:
        ...

    def query_languages(self) -> QuerySet[models.CrewSubmittableLanguage]:
        ...

    def query_applications(self) -> QuerySet[models.CrewApplication]:
        ...

    def query_activities(self) -> QuerySet[models.CrewActivity]:
        ...

    def query_activities_published(self) -> QuerySet[models.CrewActivity]:
        """크루원들에게 공개된 활동들"""
        ...

    def query_problems(self) -> QuerySet[Problem]:
        ...

    def query_captain(self) -> QuerySet[models.CrewMember]:
        ...

    def statistics(self) -> ProblemStatisticDTO:
        """대쉬보드에 사용되는 크루가 풀이해온 문제 통계"""
        ...

    def display_name(self) -> str:
        ...

    def tags(self) -> List[dto.CrewTag]:
        ...

    def languages(self) -> List[enums.ProgrammingLanguageChoices]:
        ...

    def min_boj_level(self) -> BOJLevel:
        ...

    def is_captain(self, user: User) -> bool:
        ...

    def is_member(self, user: User) -> bool:
        ...

    def set_languages(self, languages: List[enums.ProgrammingLanguageChoices]) -> None:
        ...

    def apply(self, applicant: User, message: str) -> models.CrewApplication:
        """지원자가 자격요건을 갖추지 못했다면 ValidationError를 발생시킬 수 있다."""
        ...
