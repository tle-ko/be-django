import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from drf_yasg.utils import swagger_auto_schema

from .proxy import Submission, SubmissionComment
from .serializers import SubmissionSerializer, SubmissionDetailSerializer, SubmissionCommentSerializer

logger = logging.getLogger(__name__)

class CreateCommentAPIView(generics.CreateAPIView):
    """
    제출된 문제에 대한 댓글을 작성하는 API
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionCommentSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: 'Created',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        # Get submission ID from URL kwargs
        submission_id = kwargs.get('submission_id')
        
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({'detail': 'Submission not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Pass submission instance and current user to the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(submission=submission, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateSubmissionAPIView(generics.CreateAPIView):
    """
    문제에 대한 코드를 제출하는 API
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: 'Created',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmissionDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SubmissionDetailSerializer
    lookup_field = 'id'
    queryset = Submission.objects.all()

class DeleteSubmissionAPIView(generics.DestroyAPIView):
    """
    제출된 코드를 삭제하는 API
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Submission.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'No Content',
            status.HTTP_404_NOT_FOUND: 'Submission not found.',
        }
    )
    def delete(self, request, *args, **kwargs):
        
        return self.destroy(request, *args, **kwargs)
    
class DeleteCommentAPIView(generics.DestroyAPIView):
    """
    제출된 코드에 대한 댓글을 삭제하는 API
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionCommentSerializer
    queryset = SubmissionComment.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'No Content',
            status.HTTP_404_NOT_FOUND: 'Comment not found.',
        }
    )
    def delete(self, request, *args, **kwargs):
       
        return self.destroy(request, *args, **kwargs)
