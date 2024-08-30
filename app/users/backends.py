from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from users.models import User


class UserAuthBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        try:
            user = User.objects.filter(username=username).get()
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        else:
            return None
