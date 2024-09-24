from rest_framework import generics

from . import proxy


class CrewApplicationUrlKwargMixin:
    queryset = proxy.CrewApplication
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    def get_crew_application(self: generics.GenericAPIView) -> proxy.CrewApplication:
        return proxy.CrewApplication.objects.get(pk=self.kwargs[self.lookup_url_kwarg])

    def get_object(self) -> proxy.CrewApplication:
        return self.get_crew_application()
