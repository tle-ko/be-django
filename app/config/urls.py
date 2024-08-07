from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import crews.views
import problems.views
import users.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include([
        path("auth/signin", users.views.SignInAPIView.as_view()),
        path("auth/signup", users.views.SignUpAPIView.as_view()),
        path("auth/signout", users.views.SignOutAPIView.as_view()),
        path("auth/verification/code", users.views.EmailVerificationCodeAPIView.as_view()),
        path("auth/verification/token", users.views.EmailVerificationTokenAPIView.as_view()),
        path("crews/", crews.views.CrewCreate.as_view()),
        path("crews/recruiting", crews.views.CrewRecruiting.as_view()),
        path("crews/my", crews.views.CrewJoined.as_view()),
        path("crews/<int:id>/detail", crews.views.CrewDetail.as_view()),
        path("problems/", problems.views.ProblemCreate.as_view()),
        path("problems/search", problems.views.ProblemSearch.as_view()),
        path("problems/<int:id>/detail", problems.views.ProblemDetail.as_view()),
        path("users/current", users.views.CurrentUserAPIView.as_view()),
    ])),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
