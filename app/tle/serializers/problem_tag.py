from rest_framework.serializers import *

from tle.models import ProblemTag


class ProblemTagSerializer(ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = [
            ProblemTag.field_name.KEY,
            ProblemTag.field_name.NAME_KO,
            ProblemTag.field_name.NAME_EN,
        ]
        read_only_fields = ['__all__']
