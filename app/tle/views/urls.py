from django.urls import include, path

from tle.views.viewsets import *


urlpatterns = [
    path("problems/", include([
        path("", ProblemViewSet.as_view({"post": "create"})),
        path("search", ProblemViewSet.as_view({"get": "list"})),
        path("<int:id>/", include([
            path("detail", ProblemViewSet.as_view({
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }))
        ])),
    ])),
    path("crews/", include([
        path("", CrewViewSet.as_view({"post": "create"})),
        path("recruiting", CrewViewSet.as_view({"get": "list_recruiting"})),
        path("my", CrewViewSet.as_view({"get": "list_my"})),
        path("<int:id>/", include([
            path("detail", CrewViewSet.as_view({
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }))
        ])),
    ])),
]
