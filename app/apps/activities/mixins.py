from rest_framework.generics import GenericAPIView

from apps.crews.mixins import CrewUrlKwargMixin

from . import models


class CrewActivityProblemUrlKwargMixin(GenericAPIView):
    queryset = models.CrewActivityProblemDAO
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    def get_object(self) -> models.CrewActivityProblemDAO:
        return super().get_object()
