from django.urls import path

from .views import UserViewSet


urlpatterns = [
    path("signin", UserViewSet.as_view({
        "post": "sign_in",
    })),
    path("signup", UserViewSet.as_view({
        "post": "sign_up",
    })),
    path("signout", UserViewSet.as_view({
        "get": "sign_out",
    })),
]
