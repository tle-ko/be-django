from http import HTTPStatus

from django.contrib.auth import (
    authenticate as django_authenticate,
    login,
    logout,
)
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import (
    UserSerializer,
    UserSignInSerializer,
    UserSignUpSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'sign_up':
            return UserSignUpSerializer(*args, **kwargs)
        if self.action == 'sign_in':
            return UserSignInSerializer(*args, **kwargs)
        return UserSerializer(*args, **kwargs)

    def sign_up(self, request: Request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.validated_data)
        # TODO: User already exists error handling

        serializer.instance = user
        return Response(serializer.data)

    def sign_in(self, request: Request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')

        login(request, user)

        serializer.instance = user
        return Response(serializer.data)

    def sign_out(self, request: Request):
        logout(request)
        return Response(status=HTTPStatus.OK)


def authenticate(request: Request, email: str, password: str) -> User:
    # TODO: User Manager 를 이용해서 authenticate 하도록 모델을 수정한 후, 이 프록시 메소드를 제거할 것.
    queryset = User.objects.filter(email=email)
    if not queryset.exists():
        return None
    username = queryset.first().username
    user = django_authenticate(request, username=username, password=password)
    return user
