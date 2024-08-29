from django.urls import include
from django.urls import path

import crews.views
# import crews.applications.views


urlpatterns = [
    path("crews/my", crews.views.MyCrewListAPIView.as_view()),
    path("crews/recruiting", crews.views.RecruitingCrewListAPIView.as_view()),
    path("crew", crews.views.CrewCreateAPIView.as_view()),
    path("crew/<int:crew_id>", include([
        path("/dashboard", crews.views.CrewDashboardAPIView.as_view()),
        path("/statistics", crews.views.CrewStatisticsAPIView.as_view()),
        # path("/applications", crews.applications.views.CrewApplicationForCrewListAPIView.as_view()),
        # path("/apply", crews.applications.views.CrewApplicantionCreateAPIView.as_view()),
    ])),
    # path("crew/applications/my", crews.applications.views.CrewApplicationForUserListAPIView.as_view()),
    # path("crew/application/<int:application_id>", include([
    #     path("/accept", crews.applications.views.CrewApplicantionAcceptAPIView.as_view()),
    #     path("/reject", crews.applications.views.CrewApplicantionRejectAPIView.as_view()),
    # ])),
    # path("crew/activities/<int:activity_id>", include([
    #     path("/dashboard", views.CrewDashboardActivityAPIView.as_view()),
    # ])),
]
