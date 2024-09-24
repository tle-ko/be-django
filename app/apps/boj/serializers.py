from rest_framework import serializers


class BOJLevelDTOSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    name = serializers.CharField()


class BOJUserDTOSerializer(serializers.Serializer):
    username = serializers.CharField()
    profile_url = serializers.CharField()
    level = BOJLevelDTOSerializer()
    rating = serializers.IntegerField()
    updated_at = serializers.DateTimeField()


class BOJTagDTOSerializer(serializers.Serializer):
    key = serializers.CharField()
    name_ko = serializers.CharField()
    name_en = serializers.CharField()
