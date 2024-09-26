from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from users.models import User


class UserAuthBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, email=None, username=None, password=None, **kwargs):
        if email is None and username is not None:
            return self.authenticate(request, email=username, password=password)
        try:
            user = User.objects.filter(email=email).get()
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        else:
            return None
