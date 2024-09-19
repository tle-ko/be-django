from django.urls import include
from django.urls import path

from . import views


urlpatterns = [
    path("crews/my", views.MyCrewListAPIView.as_view()),
    path("crews/recruiting", views.RecruitingCrewListAPIView.as_view()),
    path("crew", views.CrewCreateAPIView.as_view()),
    path("crew/<int:crew_id>", views.CrewRetrieveUpdateAPIView.as_view()),
    path("crew/<int:crew_id>/applications", views.CrewApplicationListAPIView.as_view()),
    path("crew/<int:crew_id>/statistics", views.CrewStatisticsAPIView.as_view()),
    # path("/apply", crews.applications.views.CrewApplicantionCreateAPIView.as_view()),
    # path("crew/applications/my", crews.applications.views.CrewApplicationForUserListAPIView.as_view()),
    # path("crew/application/<int:application_id>", include([
    #     path("/accept", crews.applications.views.CrewApplicantionAcceptAPIView.as_view()),
    #     path("/reject", crews.applications.views.CrewApplicantionRejectAPIView.as_view()),
    # ])),
    # path("crew/activities/<int:activity_id>", include([
    #     path("/dashboard", views.CrewDashboardActivityAPIView.as_view()),
    # ])),
]
