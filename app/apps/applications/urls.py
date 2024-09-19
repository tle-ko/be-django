from django.urls import path

from . import views


urlpatterns = [
    path("crew/application", views.CrewApplicationCreateAPIView.as_view()),
    path("crew/application/<int:application_id>/accept", views.CrewApplicantionAcceptAPIView.as_view()),
    path("crew/application/<int:application_id>/reject", views.CrewApplicantionRejectAPIView.as_view()),
]
