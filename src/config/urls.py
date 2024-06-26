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
from django.urls import (
    include,
    path,
)

from core.views import *
from crew.views import *
from problem.views import *
from user.views import *


VIEW_PLACE_HOLDER = lambda request: NotImplemented


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("v1/", include([
            path("account/", include([
                path("signup", UserAPIView.SignUp.as_view()), # 회원가입 기능 구현
                path("signin", UserAPIView.SignIn.as_view()), # 로그인 기능 구현
                path("signout", UserAPIView.SignOut.as_view()), # 로그아웃 기능 구현
            ])),
            path("user/", include([
                path("", UserAPIView.List.as_view()), # 사용자 목록 조회 기능 구현 (관리자용)
                path("<int:id>/", include([
                    path("", VIEW_PLACE_HOLDER), # TODO: 사용자 상세 조회+수정 기능 구현 (관리자용)
                ])),
            ])),
            path("problem/", include([
                path("", ProblemAPIView.ListCreate.as_view()), # 전체 문제 목록 조회(관리자용) + 생성 기능
                path("my", ProblemAPIView.MyList.as_view()), # 내가 만든 문제 목록 조회 기능 구현
                path("<int:id>/", include([
                    path("", ProblemAPIView.RetrieveUpdateDestroy.as_view()), # 문제 상세 조회 기능 구현
                    path("analysis", ProblemAnalysisAPIView.Retrieve.as_view()), # 문제 분석 조회 기능 구현
                ])),
            ])),
            path("crew/", include([
                path("", CrewAPIView.ListCreate.as_view()), # 전체 크루 목록 조회(관리자용) + 생성
                path("my", CrewAPIView.MyList.as_view()), # TODO: 내가 속한 크루 목록 조회 기능 구현
                path("recruiting", CrewAPIView.RecruitingList.as_view()), # 크루원을 모집 중인 크루 목록 조회 기능 구현
                path("<int:id>/", include([
                    path("", CrewAPIView.RetrieveUpdateDestroy.as_view()), # 크루 상세 조회(공지사항, 크루원 목록, 해결한 문제들의 태그 분포, 이번 주 현황, 모집 시작/종료/옵션, ...)+수정 기능 구현
                    path("activities", VIEW_PLACE_HOLDER), # TODO: 크루의 활동 회차 목록 조회 기능 구현
                    path("problems", VIEW_PLACE_HOLDER), # TODO: 크루에 속한 문제 목록 조회 기능 구현
                    path("pending", VIEW_PLACE_HOLDER), # TODO: 크루 가입 대기자 목록 조회 기능 구현
                ])),
            ])),
            path("activity/", include([
                path("", VIEW_PLACE_HOLDER), # TODO: 크루 활동 회차 목록 조회 + 추가(방장만) 기능 구현
                path("<int:id>/", include([
                    path("", VIEW_PLACE_HOLDER), # TODO: 크루 활동 회차 상세 조회 기능 구현
                ])),
            ])),
            path("submission/", include([
                path("", VIEW_PLACE_HOLDER), # TODO: 크루 활동 문제에 대한 풀이 제출 + 목록 조회 기능 구현
                path("<int:id>/", include([
                    path("", VIEW_PLACE_HOLDER), # TODO: 제출 상세 조회+수정 기능 구현
                ])),
            ])),
            path("comment/",include([
                path("", VIEW_PLACE_HOLDER), # TODO: 코멘트 목록 조회(관리자용) + 생성 기능 구현
                path("<int:id>/", include([
                    path("", VIEW_PLACE_HOLDER), # TODO: 코멘트 상세 조회+수정+삭제 기능 구현
                ])),
            ])),
            path("tag/", include([
                path("", TagAPIView.ListCreate.as_view()), # 전체 태그 목록 조회(관리자용) + 생성 기능
            ])),
            path("language/", include([
                path("", LanguageAPIView.ListCreate.as_view()), # 전체 언어 목록 조회(관리자용) + 생성 기능
            ])),
        ])),
    ])),
]

# Static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TODO: Remove above line in production (미디어 파일은 S3 같은 외부 의존성으로 변경하기)
