from django.urls import include, path

from tle.views.viewsets import *


urlpatterns = [
    path("auth/", include([
        path("signin", AuthViewSet.as_view({"post": "sign_in"})),
        path("signup", AuthViewSet.as_view({"post": "sign_up"})),
        path("signout", AuthViewSet.as_view({"get": "sign_out"})),
    ])),
    path("user/current", UserViewSet.as_view({"get": "current"})),
    path("user/", include([
        path("search", UserViewSet.as_view({"get": "list"})),
        path("<int:id>/", include([
            path("profile", UserViewSet.as_view({
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            })),
        ])),
    ])),
    path("problem/", include([
        path("", ProblemViewSet.as_view({"post": "create"})),
        path("search", ProblemViewSet.as_view({"get": "list"})),
        path("<int:id>/", include([
            path("description", ProblemViewSet.as_view({
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }))
        ])),
    ])),
]
