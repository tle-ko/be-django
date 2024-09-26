from rest_framework.generics import GenericAPIView

from . import dto
from . import proxy


class CrewUrlKwargMixin(GenericAPIView):
    queryset = proxy.Crew
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self) -> proxy.Crew:
        return super().get_object()


class CrewDTOUrlKwargMixin(CrewUrlKwargMixin):
    def get_object(self) -> dto.CrewDTO:
        return super().get_object().as_dto()
