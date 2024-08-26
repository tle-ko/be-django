from rest_framework import serializers

from problems import enums
from problems import models
from problems import services


class MemoryLimitField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        unit = enums.Unit(problem.memory_limit_unit)
        return {
            "value": problem.memory_limit,
            "unit": {
                "name": unit.label,
                "abbr": unit.value,
            },
        }


class TimeLimitField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        unit = enums.Unit(problem.time_limit_unit)
        return {
            "value": problem.time_limit,
            "unit": {
                "name": unit.label,
                "abbr": unit.value,
            },
        }


class DifficultyField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        service = services.get_problem_service(problem)
        return {
            "name_ko": service.difficulty().get_name(lang='ko'),
            "name_en": service.difficulty().get_name(lang='en'),
            'value': service.difficulty().value,
        }


class AnalysisField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        service = services.get_problem_service(problem)
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
                for tag in service.query_tags()
            ],
            'is_analyzed': service.is_analyzed(),
        }
