from rest_framework import serializers

from apps.problems.serializers import ProblemDTOSerializer
from apps.submissions.serializers import SubmissionDTOSerializer

from . import proxy


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


class CrewActivityDAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = proxy.CrewActivity
        fields = [
            proxy.CrewActivity.field_name.NAME,
            proxy.CrewActivity.field_name.START_AT,
            proxy.CrewActivity.field_name.END_AT,
        ]

    @property
    def data(self):
        self.instance: proxy.CrewActivity
        return CrewActivityDTOSerializer(self.instance.as_dto()).data
