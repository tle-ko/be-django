from rest_framework import generics

from . import models


class CrewUrlKwargMixin:
    queryset = models.Crew
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_crew(self: generics.GenericAPIView) -> models.Crew:
        return CrewUrlKwargMixin.queryset.objects.get(pk=self.kwargs[self.lookup_url_kwarg])
