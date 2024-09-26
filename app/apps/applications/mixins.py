from rest_framework.generics import GenericAPIView

from apps.crews.mixins import CrewUrlKwargMixin

from . import dto
from . import proxy


class CrewApplicationUrlKwargMixin(GenericAPIView):
    queryset = proxy.CrewApplication
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_object(self) -> proxy.CrewApplication:
        return super().get_object()
