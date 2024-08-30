from rest_framework import serializers

from crews.activities.models import CrewActivity


PK = 'id'


class CrewActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewActivity
        fields = [
            CrewActivity.field_name.NAME,
            CrewActivity.field_name.START_AT,
            CrewActivity.field_name.END_AT,
        ]
        read_only_fields = ['__all__']


# class CrewActivityProblemSerializer(serializers.ModelSerializer):
#     problems = fields.CrewAcitivityProblemsField()

#     class Meta:
#         model = CrewActivity
#         fields = [
#             CrewActivity.field_name.NAME,
#             CrewActivity.field_name.START_AT,
#             CrewActivity.field_name.END_AT,
#             'problems',
#         ]
#         read_only_fields = ['__all__']
