from django.urls import path

from . import views


urlpatterns = [
    path("crews/my", views.MyCrewListAPIView.as_view()),
    path("crews/recruiting", views.RecruitingCrewListAPIView.as_view()),
    path("crew", views.CrewCreateAPIView.as_view()),

    path("crew/<int:crew_id>", views.CrewRetrieveUpdateAPIView.as_view()),
    path("crew/<int:crew_id>/statistics", views.CrewStatisticsAPIView.as_view()),
    path("crew/<int:crew_id>/applications", views.CrewApplicationListAPIView.as_view()),
    path("crew/<int:crew_id>/apply", views.CrewApplicationCreateAPIView.as_view()),
    path("crew/<int:crew_id>/activity", views.CrewActivityCreateAPIView.as_view()),

    path("crew/activity/<int:activity_id>", views.CrewActivityRetrieveUpdateAPIView.as_view()),

    path("crew/application/<int:application_id>/accept", views.CrewApplicantionAcceptAPIView.as_view()),
    path("crew/application/<int:application_id>/reject", views.CrewApplicantionRejectAPIView.as_view()),
    path("crew/problem/<int:problem_id>", views.CrewActivityProblemRetrieveAPIView.as_view()),
    path('crew/problem/<int:problem_id>/submit', views.CrewSubmissionCreateAPIView.as_view()),

    path('crew/submission/<int:submission_id>', views.CrewSubmissionRetrieveDestroyAPIView.as_view()),
    path('crew/submission/<int:submission_id>/comment', views.CrewSubmissionCommentCreateAPIView.as_view()),

    path('crew/submission/comment/<int:comment_id>', views.CrewSubmissionCommentDestroyAPIView.as_view()),
]
