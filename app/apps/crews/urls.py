from django.urls import path

from . import views


urlpatterns = [
    path("crews/my", views.MyCrewListAPIView.as_view()),
    path("crews/recruiting", views.RecruitingCrewListAPIView.as_view()),
    path("crew", views.CrewCreateAPIView.as_view()),
    path("crew/<int:crew_id>", views.CrewRetrieveUpdateAPIView.as_view()),
    path("crew/<int:crew_id>/statistics", views.CrewStatisticsAPIView.as_view()),
]
