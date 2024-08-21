from rest_framework import serializers

from problems import models
from problems import services
from problems.constants import Unit


class MemoryLimitField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        return {
            "value": problem.memory_limit_megabyte,
            "unit": {
                "name_ko": Unit.MEGA_BYTE.name_ko,
                "name_en": Unit.MEGA_BYTE.name_en,
                "abbr": Unit.MEGA_BYTE.abbr,
            },
        }


class TimeLimitField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        return {
            "value": problem.time_limit_second,
            "unit": {
                "name_ko": Unit.SECOND.name_ko,
                "name_en": Unit.SECOND.name_en,
                "abbr": Unit.SECOND.abbr,
            },
        }


class DifficultyField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        service = services.ProblemAnalysisService.from_problem(problem)
        return {
            "name_ko": service.difficulty().get_name(lang='ko'),
            "name_en": service.difficulty().get_name(lang='en'),
            'value': service.difficulty().value,
        }


class AnalysisField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        service = services.ProblemAnalysisService.from_problem(problem)
        return {
            'difficulty': {
                "name_ko": service.difficulty().get_name(lang='ko'),
                "name_en": service.difficulty().get_name(lang='en'),
                'value': service.difficulty().value,
                'description': service.difficulty_description(),
            },
            'time_complexity': {
                'value': service.time_complexity(),
                'description': service.time_complexity_description(),
            },
            'hints': service.hints(),
            'tags': [
                {
                    'key': tag.key,
                    'name_en': tag.name_en,
                    'name_ko': tag.name_ko,
                }
                for tag in service.tags()
            ],
            'is_analyzed': service.is_analyzed(),
        }
