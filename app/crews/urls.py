from django.urls import include
from django.urls import path

from crews import views


urlpatterns = [
    path("crews/my", views.MyCrewListAPIView.as_view()),
    path("crews/recruiting", views.RecruitingCrewListAPIView.as_view()),
    path("crew", views.CrewCreateAPIView.as_view()),
    path("crew/<int:crew_id>", include([
        path("/dashboard", views.CrewDashboardAPIView.as_view()),
        path("/statistics", views.CrewStatisticsAPIView.as_view()),
        path("/applications", views.CrewApplicationListAPIView.as_view()),
        path("/apply", views.CrewApplicantionCreateAPIView.as_view()),
    ])),
    path("crew/applications/my", views.CrewApplicantionRejectAPIView.as_view()),
    path("crew/application/<int:application_id>", include([
        path("/accept", views.CrewApplicantionAcceptAPIView.as_view()),
        path("/reject", views.CrewApplicantionRejectAPIView.as_view()),
    ])),
    path("crew/activities/<int:activity_id>", include([
        path("/dashboard", views.CrewDashboardActivityAPIView.as_view()),
    ])),
]
