from rest_framework import generics

from .models import proxy


class CrewActivityUrlKwargMixin:
    queryset = proxy.CrewActivity
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    def get_activity(self: generics.GenericAPIView) -> proxy.CrewActivity:
        return CrewActivityUrlKwargMixin.queryset.objects.get(pk=self.kwargs[self.lookup_url_kwarg])
