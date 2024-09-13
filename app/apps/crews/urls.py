from django.urls import include
from django.urls import path

from apps.crews.views import MyCrewListAPIView
from apps.crews.views import RecruitingCrewListAPIView
from apps.crews.views import CrewCreateAPIView
from apps.crews.views import CrewDashboardAPIView
from apps.crews.views import CrewStatisticsAPIView
from apps.crews.submissions.views import CodeReviewInquiryAPI


urlpatterns = [
    path("crews/my", MyCrewListAPIView.as_view()),
    path("crews/recruiting", RecruitingCrewListAPIView.as_view()),
    path('crew/<int:crew_id>/code-review/<int:user_id>/', CodeReviewInquiryAPI.as_view(), name='code-review-inquiry'),
    path("crew/<int:crew_id>", include([
        path("/dashboard", CrewDashboardAPIView.as_view()),
        path("/statistics", CrewStatisticsAPIView.as_view()),
         
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
