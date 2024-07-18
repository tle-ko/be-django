from django.urls import include, path

from tle.views.viewsets import *


urlpatterns = [
    path("account/", include([
        path("signin", UserViewSet.as_view({"post": "sign_in"})),
        path("signup", UserViewSet.as_view({"post": "sign_up"})),
        path("signout", UserViewSet.as_view({"get": "sign_out"})),
        path("current", UserViewSet.as_view({"get": "current"})),
    ])),
    path("problem", ProblemViewSet.as_view({
        "post": "create",
        "get": "list",
    })),
    path("problem/", include([
        path("<int:id>", ProblemViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        })),
    ])),
]
