from rest_framework import serializers

from boj.enums import BOJLevel
from boj.models import BOJUser


class BOJLevelField(serializers.SerializerMethodField):
    def to_representation(self, boj_level: BOJLevel):
        return {
            'value': boj_level.value,
            'name': boj_level.get_name(lang='ko', arabic=False),
        }

    def get_attribute(self, instance: BOJUser) -> BOJLevel:
        assert isinstance(instance, BOJUser)
        return BOJLevel(instance.level)


class BOJProfileUrlField(serializers.SerializerMethodField):
    def to_representation(self, username: str):
        return f'https://boj.kr/{username}'

    def get_attribute(self, instance: BOJUser) -> str:
        assert isinstance(instance, BOJUser)
        return instance.username


class BOJUserSerializer(serializers.ModelSerializer):
    level = BOJLevelField()
    profile_url = BOJProfileUrlField()

    class Meta:
        model = BOJUser
        fields = [
            BOJUser.field_name.USERNAME,
            'profile_url',
            'level',
            BOJUser.field_name.RATING,
            BOJUser.field_name.UPDATED_AT,
        ]
