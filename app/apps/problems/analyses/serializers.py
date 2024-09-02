from typing import List

from django.db.models import QuerySet
from rest_framework import serializers

from apps.problems.analyses.enums import ProblemDifficulty
from apps.problems.analyses.models import ProblemAnalysis
from apps.problems.analyses.models import ProblemAnalysisTag
from apps.problems.analyses.models import ProblemTag


PK = 'id'


class ProblemAnalysisDifficultyField(serializers.SerializerMethodField):
    def to_representation(self, difficulty: ProblemDifficulty):
        return {
            "name_ko": difficulty.get_name(lang='ko'),
            "name_en": difficulty.get_name(lang='en'),
            'value': difficulty.value,
        }

    def get_attribute(self, instance: ProblemAnalysis) -> ProblemDifficulty:
        assert isinstance(instance, ProblemAnalysis)
        return ProblemDifficulty(instance.difficulty)


class ProblemAnalysisTimeComplexityField(serializers.SerializerMethodField):
    def to_representation(self, value: str):
        return {
            'value': value,
        }

    def get_attribute(self, instance: ProblemAnalysis):
        assert isinstance(instance, ProblemAnalysis)
        return instance.time_complexity


class ProblemAnalysisTagsField(serializers.SerializerMethodField):
    def to_representation(self, tags: QuerySet[ProblemTag]):
        return ProblemTagSerializer(tags, many=True).data

    def get_attribute(self, instance: ProblemAnalysis):
        assert isinstance(instance, ProblemAnalysis)
        tag_ids = ProblemAnalysisTag.objects.analysis(instance).values_list(ProblemAnalysisTag.field_name.TAG, flat=True)
        return ProblemTag.objects.filter(pk__in=tag_ids)


class ProblemAnalysisHintsField(serializers.SerializerMethodField):
    def to_representation(self, hints: List[str]):
        return hints

    def get_attribute(self, instance: ProblemAnalysis) -> List[str]:
        assert isinstance(instance, ProblemAnalysis)
        if isinstance(instance.hint, list):
            return instance.hint
        return [instance.hint]


class ProblemAnalysisSerializer(serializers.ModelSerializer):
    difficulty = ProblemAnalysisDifficultyField()
    time_complexity = ProblemAnalysisTimeComplexityField()
    tags = ProblemAnalysisTagsField()
    hints = ProblemAnalysisHintsField()

    class Meta:
        model = ProblemAnalysis
        fields = [
            'difficulty',
            'time_complexity',
            'tags',
            'hints',
            ProblemAnalysis.field_name.CREATED_AT,
        ]
        read_only_fields = ['__all__']


class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = [
            ProblemTag.field_name.KEY,
            ProblemTag.field_name.NAME_EN,
            ProblemTag.field_name.NAME_KO,
        ]
        read_only_fields = ['__all__']
