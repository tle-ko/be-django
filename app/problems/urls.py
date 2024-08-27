from django.urls import path

from problems import views


urlpatterns = [
    path("problems", views.ProblemSearchListAPIView.as_view()),
    path("problem", views.ProblemCreateAPIView.as_view()),
    path("problem/<int:id>/detail", views.ProblemDetailRetrieveUpdateDestroyAPIView.as_view()),
]
