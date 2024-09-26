from django.urls import path

from . import views


urlpatterns = [
    path("crew/<int:crew_id>/activity", views.CrewActivityCreateAPIView.as_view()),
    path("crew/activity/<int:activity_id>", views.CrewActivityRetrieveUpdateAPIView.as_view()),
    path("crew/activity/problem/<int:problem_id>", views.CrewActivityProblemRetrieveAPIView.as_view()),
]
