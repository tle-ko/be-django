from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *

from config.permissions import ReadOnly

from .models import *
from .serializers import *


class _PageNumberPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = 'page_size'


class TagAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Tag.objects.all()
        serializer_class = TagSerializer
        permission_classes = [IsAdminUser | (IsAuthenticated & ReadOnly)]
        pagination_class = _PageNumberPagination


class LanguageAPIView:
    class ListCreate(ListCreateAPIView):
        queryset = Language.objects.all()
        serializer_class = LanguageSerializer
        permission_classes = [IsAdminUser | (IsAuthenticated & ReadOnly)]
        pagination_class = _PageNumberPagination
