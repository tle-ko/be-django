from django.urls import path
from .views import (
    CreateSubmissionAPIView,
    SubmissionDetailAPIView,
    CreateCommentAPIView,
    DeleteSubmissionAPIView,
    DeleteCommentAPIView,
)

urlpatterns = [

    path('submissions/', CreateSubmissionAPIView.as_view(), name='create-submission'),
    path('submissions/<int:id>/', SubmissionDetailAPIView.as_view(), name='submission-detail'),
    path('submissions/<int:id>/delete/', DeleteSubmissionAPIView.as_view(), name='delete-submission'),
    path('submissions/<int:submission_id>/comments/', CreateCommentAPIView.as_view(), name='create-comment'),
    path('submissions/<int:submission_id>/comments/<int:id>/delete/', DeleteCommentAPIView.as_view(), name='delete-comment'),
]
