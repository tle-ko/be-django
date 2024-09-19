from rest_framework import serializers

from apps.problems.serializers import ProblemDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer


class CrewActivityProblemDTOSerializer(ProblemDTOSerializer):
    problem_ref_id = serializers.IntegerField()
    order = serializers.IntegerField()


class CrewActivityProblemDetailDTOSerializer(CrewActivityProblemDTOSerializer):
    submissions = SubmissionDTOSerializer(many=True)
    my_submission = SubmissionDTOSerializer(required=False, default=None)


class CrewActivityDTOSerializer(serializers.Serializer):
    activity_id = serializers.IntegerField()
    name = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    is_in_progress = serializers.BooleanField()
    has_started = serializers.BooleanField()
    has_ended = serializers.BooleanField()


class CrewActivityDetailDTOSerializer(CrewActivityDTOSerializer):
    problems = CrewActivityProblemDetailDTOSerializer(many=True)
