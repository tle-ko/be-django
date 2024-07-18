from datetime import datetime

from tle.models import *
from tle.services.data.parser.base import ModelParser


class ProblemParser(ModelParser[Problem]):
    def perform_parse(self, item: dict) -> Problem:
        return Problem.objects.create(
            title=item['title'],
            link=item['link'],
            description=item['description'],
            input_description=item['input_description'],
            output_description=item['output_description'],
            time_limit=item['time_limit'],
            memory_limit=item['memory_limit'],
            created_at=datetime.fromisoformat(item['created_at']),
            updated_at=datetime.fromisoformat(item['updated_at']),
        )


class ProblemTagParser(ModelParser[ProblemTag]):
    def perform_parse(self, item: dict) -> ProblemTag:
        return ProblemTag.objects.create(
            pk=item['bojTagId'],
            parent=None,
            key=item['key'],
            name_ko=self._find(item['displayNames'], 'ko')['name'],
            name_en=self._find(item['displayNames'], 'en')['name'],
        )

    def _find(self, display_names: list[dict], language: str) -> dict:
        return next(filter(lambda x: x['language'] == language, display_names))


class SubmissionLanguageParser(ModelParser[SubmissionLanguage]):
    def perform_parse(self, item: dict) -> SubmissionLanguage:
        return SubmissionLanguage.objects.create(
            pk=item['bojId'],
            key=item['key'],
            name=item['displayName'],
            extension=item['extension'],
        )
