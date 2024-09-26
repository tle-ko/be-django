from django.urls import path

from . import views

urlpatterns = [
    path('crew/activity/problem/<int:problem_id>/submission', views.SubmissionCreateAPIView.as_view()),
    path('crew/activity/problem/submission/<int:submission_id>', views.SubmissionRetrieveDestroyAPIView.as_view()),
    path('crew/activity/problem/submission/<int:submission_id>/comment', views.SubmissionCommentCreateAPIView.as_view()),
    path('crew/activity/problem/submission/comment/<int:comment_id>', views.SubmissionCommentDestroyAPIView.as_view()),
]
