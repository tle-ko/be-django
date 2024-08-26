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
        path("crews/my", crews.views.MyCrewListAPIView.as_view()),
        path("crews/recruiting", crews.views.RecruitingCrewListAPIView.as_view()),
        path("crew", crews.views.CrewCreateAPIView.as_view()),
        path("crew/<int:crew_id>/dashboard", crews.views.CrewDashboardAPIView.as_view()),
        path("crew/<int:crew_id>/statistics", crews.views.CrewStatisticsAPIView.as_view()),
        path("crew/<int:crew_id>/apply", crews.views.CrewApplicantionCreateAPIView.as_view()),
        path("crew/<int:crew_id>/applications", crews.views.CrewApplicationsListAPIView.as_view()),
        path("crew/applications/my", crews.views.CrewApplicantionRejectAPIView.as_view()),
        path("crew/application/<int:application_id>/accept", crews.views.CrewApplicantionAcceptAPIView.as_view()),
        path("crew/application/<int:application_id>/reject", crews.views.CrewApplicantionRejectAPIView.as_view()),
        path("crew/activities/<int:activity_id>/dashboard", crews.views.CrewActivityRetrieveAPIView.as_view()),
        path("problems", problems.views.ProblemSearchListAPIView.as_view()),
        path("problem", problems.views.ProblemCreateAPIView.as_view()),
        path("problem/<int:id>/detail", problems.views.ProblemDetailRetrieveUpdateDestroyAPIView.as_view()),
        path("user/manage", users.views.CurrentUserRetrieveUpdateAPIView.as_view()),
        path("submissions/<int:id>", submissions.views.CreateCodeReview.as_view()),
    ])),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
