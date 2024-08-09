from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import crews.views
import problems.views
import users.views


schema_view = get_schema_view(
    info=openapi.Info(
        title="Time Limit Exceeded API Server",
        default_version='1.0.0',
        description="",
        contact=openapi.Contact(email="202115064@sangmyung.kr"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include([
        path("auth/signin", users.views.SignInAPIView.as_view()),
        path("auth/signup", users.views.SignUpAPIView.as_view()),
        path("auth/signout", users.views.SignOutAPIView.as_view()),
        path("auth/username/check", users.views.UsernameCheckAPIView.as_view()),
        path("auth/email/check", users.views.EmailCheckAPIView.as_view()),
        path("auth/email/verify", users.views.EmailVerifyAPIView.as_view()),
        path("crews/", crews.views.CrewCreate.as_view()),
        path("crews/recruiting", crews.views.CrewRecruiting.as_view()),
        path("crews/my", crews.views.CrewJoined.as_view()),
        path("crews/<int:id>/detail", crews.views.CrewDetail.as_view()),
        path("problems/", problems.views.ProblemCreate.as_view()),
        path("problems/search", problems.views.ProblemSearch.as_view()),
        path("problems/<int:id>/detail", problems.views.ProblemDetail.as_view()),
        path("users/current", users.views.CurrentUserAPIView.as_view()),
        path("submissions/<int:id>", submissions.views.CreateCodeReview.as_view()),
    ])),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
