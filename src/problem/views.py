from rest_framework.generics import *
from rest_framework.permissions import *

from .models import *
from .serializers import *


class IsProblemCreator(BasePermission):
    def has_object_permission(self, request, view, obj: Problem) -> bool:
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.user == request.user
        )


class ProblemAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Problem.objects.all()
        serializer_class = ProblemSerializer
        permission_classes = [IsAuthenticated]

    class RetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Problem.objects.all()
        serializer_class = ProblemSerializer
        permission_classes = [IsAuthenticatedOrReadOnly] # TODO: 본인만 수정 가능하게 수정
        lookup_url_kwarg = 'id'


class ProblemAnalysisAPIView:
    class Retrieve(RetrieveAPIView):
        queryset = ProblemAnalysis.objects.all()
        serializer_class = ProblemAnalysisSerializer
        lookup_url_kwarg = 'id'
        lookup_field = 'problem__id'
