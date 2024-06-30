from django.urls import include, path

from .views import *


urlpatterns = [
    path("", ProblemViewSet.as_view({
        "get": "list",
        "post": "create",
    })),
    path("my/", ProblemViewSet.as_view({
        "get": "my_list",
    })),
    path("<int:pk>/", include([
        path("", ProblemViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        })),
        path("analysis", AnalysisViewSet.as_view({
            "get": "retrieve",
        })),
    ])),
    path("language/", include([
        path("", LanguageViewSet.as_view({
            "get": "list",
            "post": "create",
        })),
        path("<int:pk>/", LanguageViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        })),
    ])),
    path("tag/", include([
        path("", TagViewSet.as_view({
            "get": "list",
            "post": "create",
        })),
        path("<int:pk>/", TagViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        })),
    ])),
]
