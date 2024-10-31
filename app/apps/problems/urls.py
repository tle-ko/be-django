from django.urls import path

from apps.problems import views


urlpatterns = [
    path("problems", views.ProblemSearchListAPIView.as_view()),
    path("problem", views.ProblemCreateAPIView.as_view()),
    path("problem/<int:problem_ref_id>/detail", views.ProblemDetailRetrieveUpdateDestroyAPIView.as_view()),
]
