from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import crews.urls
import problems.urls
import users.views
import submissions.views


schema_view = get_schema_view(
    info=openapi.Info(
        title="Time Limit Exceeded API Server",
        default_version='1.0.0',
        description="",
        contact=openapi.Contact(email="202115064@sangmyung.kr"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
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
        *crews.urls.urlpatterns,
        *problems.urls.urlpatterns,
        path("user/manage", users.views.CurrentUserRetrieveUpdateAPIView.as_view()),
        path("submissions/<int:id>", submissions.views.CreateCodeReview.as_view()),
    ])),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
