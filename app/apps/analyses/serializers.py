from rest_framework import serializers


class ProblemTagDTOSerializer(serializers.Serializer):
    key = serializers.CharField()
    name_ko = serializers.CharField()
    name_en = serializers.CharField()


class ProblemDifficultyDTOSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    name_ko = serializers.CharField()
    name_en = serializers.CharField()


class ProblemAnalysisDTOSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    time_complexity = serializers.CharField()
    difficulty = ProblemDifficultyDTOSerializer()
    tags = ProblemTagDTOSerializer(many=True)
    hints = serializers.ListField(child=serializers.CharField())
