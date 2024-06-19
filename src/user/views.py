from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *

from .models import *
from .serializers import *


class UserAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [IsAdminUser]


    class Login(GenericAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        permission_classes = [AllowAny]

        def post(self, request: Request):
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(UserSerializer(user).data)
            return Response(status=HTTPStatus.UNAUTHORIZED)


    class Logout(GenericAPIView):
        def get(self, request: Request):
            logout(request)
            return Response(status=HTTPStatus.OK)
