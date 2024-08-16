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
        analysis = services.get_analysis(problem)
        return {
            "name_ko": analysis.difficulty.get_name(lang='ko'),
            "name_en": analysis.difficulty.get_name(lang='en'),
            'value': analysis.difficulty.value,
        }


class AnalysisField(serializers.SerializerMethodField):
    def to_representation(self, problem: models.Problem):
        assert isinstance(problem, models.Problem)
        analysis = services.get_analysis(problem)
        is_analyzed = analysis.difficulty != models.ProblemDifficultyChoices.UNDER_ANALYSIS
        tags_queryset = models.ProblemTag.objects.filter(**{
            models.ProblemTag.field_name.KEY+'__in': analysis.tags,
        })
        if not is_analyzed:
            difficulty_description = "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"
            time_complexity_description = "AI가 분석을 진행하고 있어요! [이 기능은 추가될 예정이 없습니다]"
        else:
            difficulty_description = "기초적인 계산적 사고와 프로그래밍 문법만 있어도 해결 가능한 수준 [이 기능은 추가될 예정이 없습니다]"
            time_complexity_description = "선형시간에 풀이가 가능한 문제. N의 크기에 주의하세요. [이 기능은 추가될 예정이 없습니다]"
        return {
            'difficulty': {
                "name_ko": analysis.difficulty.get_name(lang='ko'),
                "name_en": analysis.difficulty.get_name(lang='en'),
                'value': analysis.difficulty.value,
                'description': difficulty_description,
            },
            'time_complexity': {
                'value': analysis.time_complexity,
                'description': time_complexity_description,
            },
            'hint': analysis.hint,
            'tags': [
                {
                    'key': tag.key,
                    'name_en': tag.name_en,
                    'name_ko': tag.name_ko,
                }
                for tag in tags_queryset
            ],
            'is_analyzed': is_analyzed,
        }
