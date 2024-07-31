"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import *
from problems.views import ProblemCreate, ProblemDetail, ProblemSearch
from crews.views import CrewCreate, CrewDetail, CrewRecruiting, CrewJoined

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include([
        path("auth/", include([
            path("signin", SignIn.as_view()),
            path("signup", SignUp.as_view()),
            path("signout", SignOut.as_view()),
            path("verification", EmailVerification.as_view()),
        ])),
        path("users/current", CurrentUser.as_view()),
        path("problems/", include([
            path("", ProblemCreate.as_view()),
            path("search", ProblemSearch.as_view()),
            path("<int:id>/detail", ProblemDetail.as_view()),
        ])),
        path("crews/", include([
            path("", CrewCreate.as_view()),
            path("recruiting", CrewRecruiting.as_view()),
            path("my", CrewJoined.as_view()),
            path("<int:id>/detail", CrewDetail.as_view()),
        ])),
    ])),
]

# Static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Media files
# TODO: 미디어 파일은 S3 같은 외부 의존성으로 변경하기
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
