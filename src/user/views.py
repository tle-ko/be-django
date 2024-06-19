from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
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


    class SignUp(GenericAPIView):
        serializer_class = UserSignUpSerializer
        permission_classes = [AllowAny]

        def post(self, request: Request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create_user(**serializer.validated_data)
            return Response(UserSerializer(user).data)


    class SignIn(GenericAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [AllowAny]

        def post(self, request: Request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)
                assert user is not None
                login(request, user)
                return Response(UserSerializer(user).data)
            except User.DoesNotExist:
                # TODO: add logger
                pass
            except AssertionError:
                # TODO: add logger
                pass
            return Response(status=HTTPStatus.UNAUTHORIZED)


    class SignOut(GenericAPIView):
        def get(self, request: Request):
            logout(request)
            return Response(status=HTTPStatus.OK)
