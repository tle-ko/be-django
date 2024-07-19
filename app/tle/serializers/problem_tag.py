from rest_framework.serializers import *

from tle.models import ProblemTag


class ProblemTagSerializer(ModelSerializer):
    parent = SerializerMethodField()

    class Meta:
        model = ProblemTag
        fields = [
            'parent',
            'key',
            'name_ko',
            'name_en',
        ]
        read_only_fields = ['__all__']

    def get_parent(self, obj: ProblemTag):
        if obj.parent is None:
            return None
        return ProblemTagSerializer(obj.parent).data
