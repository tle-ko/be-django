from django.urls import path

from . import views


urlpatterns = [
    path("crew/activity/<int:activity_id>", views.CrewActivityRetrieveAPIView.as_view()),
    path("crew/activity/problem/<int:problem_id>", views.CrewActivityProblemRetrieveAPIView.as_view()),
]
