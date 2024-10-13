from django.urls import path

from apps.problems import views


urlpatterns = [
    path("problem_refs", views.ProblemSearchListAPIView.as_view()),
    path("problem_ref", views.ProblemCreateAPIView.as_view()),
    path("problem_ref/<int:problem_ref_id>", views.ProblemDetailRetrieveUpdateDestroyAPIView.as_view()),
]
