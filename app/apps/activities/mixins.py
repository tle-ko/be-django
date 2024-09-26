from rest_framework.generics import GenericAPIView

from . import proxy


class CrewActivityUrlKwargMixin(GenericAPIView):
    queryset = proxy.CrewActivity
    lookup_field = 'id'
    lookup_url_kwarg = 'activity_id'

    def get_object(self) -> proxy.CrewActivity:
        return super().get_object()


class CrewActivityProblemUrlKwargMixin(GenericAPIView):
    queryset = proxy.CrewActivityProblem
    lookup_field = 'id'
    lookup_url_kwarg = 'problem_id'

    def get_object(self) -> proxy.CrewActivityProblem:
        return super().get_object()
