from rest_framework.serializers import *

from tle.models import ProblemTag


class ProblemTagSerializer(ModelSerializer):
    parent = SerializerMethodField()

    class Meta:
        model = ProblemTag
        fields = [
            ProblemTag.field_name.KEY,
            ProblemTag.field_name.NAME_KO,
            ProblemTag.field_name.NAME_EN,
            ProblemTag.field_name.PARENT,
        ]
        read_only_fields = ['__all__']

    def get_parent(self, obj: ProblemTag):
        if obj.parent is None:
            return None
        return ProblemTagSerializer(obj.parent).data
