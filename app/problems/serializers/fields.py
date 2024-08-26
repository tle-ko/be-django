from rest_framework import serializers

from problems import dto
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
            },
            'time_complexity': {
                'value': service.time_complexity(),
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


class ProblemStatisticsDifficultyField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatisticDTO):
        assert isinstance(statistics, dto.ProblemStatisticDTO)
        try:
            ratio_denominator = 1 / statistics.sample_count
        except ZeroDivisionError:
            ratio_denominator = 0
        finally:
            return [
                {
                    'difficulty': difficulty,
                    'problem_count': count,
                    'ratio': count * ratio_denominator,
                }
                for difficulty, count in statistics.difficulty.items()
            ]


class ProblemStatisticsTagsField(serializers.SerializerMethodField):
    def to_representation(self, statistics: dto.ProblemStatisticDTO):
        assert isinstance(statistics, dto.ProblemStatisticDTO)
        try:
            ratio_denominator = 1 / statistics.sample_count
        except ZeroDivisionError:
            ratio_denominator = 0
        finally:
            return [
                {
                    'label': {
                        'ko': tag.name_ko,
                        'en': tag.name_en,
                    },
                    'problem_count': count,
                    'ratio': count * ratio_denominator,
                }
                for tag, count in statistics.tags.items()
            ]
