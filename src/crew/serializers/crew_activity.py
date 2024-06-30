from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from crew.models import CrewActivity


class CrewActivitySerializer(ModelSerializer):
    date = SerializerMethodField()

    class Meta:
        model = CrewActivity
        fields = (
            'name',
            'date',
        )

    def get_date(self, obj: CrewActivity):
        return {
            'start_at': obj.start_at,
            'end_at': obj.end_at,
        }
