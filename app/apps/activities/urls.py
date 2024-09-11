from django.urls import include
from django.urls import path

from apps.activities import views


urlpatterns = [
    path("crew/activity/<int:activity_id>/submissions", views.ActivitySubmissionsAPIView.as_view()),
]
