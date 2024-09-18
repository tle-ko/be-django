from rest_framework import generics

from .models import proxy


class CrewUrlKwargMixin:
    queryset = proxy.Crew
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_crew(self: generics.GenericAPIView) -> proxy.Crew:
        return CrewUrlKwargMixin.queryset.objects.get(pk=self.kwargs[self.lookup_url_kwarg])
