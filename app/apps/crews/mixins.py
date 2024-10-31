from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404

from . import models


class CrewUrlKwargMixin(GenericAPIView):
    queryset = models.CrewDAO
    lookup_field = 'id'
    lookup_url_kwarg = 'crew_id'

    def get_object(self) -> models.CrewDAO:
        queryset = self.filter_queryset(self.queryset)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
