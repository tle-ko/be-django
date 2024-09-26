from rest_framework import generics

from . import mixins
from . import serializers


class CrewActivityRetrieveAPIView(mixins.CrewActivityUrlKwargMixin, generics.RetrieveAPIView):
    """크루 활동 상세 조회 API.\n\n."""
    serializer_class = serializers.CrewActivityDetailDTOSerializer

    def get_object(self):
        return mixins.CrewActivityUrlKwargMixin.get_object(self).as_detail_dto(self.request.user)


class CrewActivityProblemRetrieveAPIView(mixins.CrewActivityProblemUrlKwargMixin, generics.RetrieveAPIView):
    """크루 활동 문제 상세 조회 API.\n\n."""
    serializer_class = serializers.CrewActivityProblemDetailDTOSerializer

    def get_object(self):
        return mixins.CrewActivityProblemUrlKwargMixin.get_object(self).as_detail_dto(self.request.user)
