from rest_framework.serializers import Serializer

from users.models import User


class CurrentUserMixin:
    def current_user(self: Serializer) -> User:
        return self.context['request'].user
