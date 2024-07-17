from django.urls import include, path

from tle.views.viewsets import *


urlpatterns = [
    path("account/", include([
        path("signin", UserViewSet.as_view({"post": "sign_in"})),
        path("signup", UserViewSet.as_view({"post": "sign_up"})),
        path("signout", UserViewSet.as_view({"get": "sign_out"})),
        path("current", UserViewSet.as_view({"get": "current"})),
    ])),
]
