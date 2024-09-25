from django.urls import path
from .views import CreateSubmissionAPIView, SubmissionDetailAPIView,CreateCommentAPIView

urlpatterns = [
    path('submission/', CreateSubmissionAPIView.as_view(), name='create-submission'),
    path('submission/<int:id>/', SubmissionDetailAPIView.as_view(), name='submission-detail'),
     path('submissions/<int:submission_id>/comments/', CreateCommentAPIView.as_view(), name='create-comment'),
]
