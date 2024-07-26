import logging

from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from users.models import User


logger = logging.getLogger(__name__)


class UserAuthBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        """username 필드지만 email로 인증하도록 오버라이드 되어있음."""
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
