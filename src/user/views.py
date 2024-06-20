from http import HTTPStatus

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *

from .models import *
from .serializers import *


class UserAPIView:
    class List(ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [IsAdminUser]


    class SignUp(CreateAPIView):
        serializer_class = UserSignUpSerializer
        permission_classes = [AllowAny]

        def perform_create(self, serializer):
            serializer.instance = User.objects.create_user(**serializer.validated_data)


    class SignIn(GenericAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [AllowAny]

        def post(self, request: Request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # TODO: authenticate()만 이용하여 email, password로 인증하는 기능 리팩토링
            username = self._get_username(serializer)
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is None:
                return Response(status=HTTPStatus.UNAUTHORIZED)

            login(request, user)

            return Response(UserSerializer(user).data)

        def _get_username(self, serializer):
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                raise AuthenticationFailed
            return user.username


    class SignOut(GenericAPIView):
        def get(self, request: Request):
            logout(request)
            return Response(status=HTTPStatus.OK)
