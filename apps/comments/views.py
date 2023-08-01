from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentDetailSerializer
from comments.permissions import CommentCreatePermission, CommentDetailPermission
from apps.core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(
        description="List an object's comments.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            404: 'Not found'
        },
        tags=['Comments']
    ),
    post=extend_schema(
        description="Create/Reply a comment.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
            404: 'Not found'
        },
        tags=['Comments']
    )
)
class CommentListCreateView(ContentObjectMixin, ListCreateAPIView):
    """
    Create And List Comments.
    """

    def get_permissions(self):
        # check if comments are allowed for object if request is POST
        if self.request.method == "POST":
            return [IsAuthenticated(), CommentCreatePermission()]
        return [IsAuthenticated()]

    serializer_class = CommentSerializer

    def get_serializer_context(self):
        """
        send user and object to serializer.
        """
        return {'user': self.request.user, 'content_object': self.get_object}

    def get_queryset(self):
        content_object = self.get_object()
        parent_comments = content_object.comments.select_related(
            'user'
        ).filter(parent__isnull=True)
        return parent_comments.order_by("-pinned", "-date")
        

@extend_schema_view(
    get=extend_schema(description="Comment detail page [replies]."),
    put=extend_schema(description="Update a comment [only by its user]."),
    patch=extend_schema(description="Update a comment [only by its user]."),
    delete=extend_schema(description="Delete a comment [by its user or channel's owner].")
)
class CommentDetailView(ContentObjectMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, CommentDetailPermission]
    serializer_class = CommentDetailSerializer

    def get_object(self):
        return get_object_or_404(
                self.object.comments.select_related('user'), 
                token=self.kwargs.get("comment_token")
            )


@extend_schema_view(
    get=extend_schema(description="Pin a comment [channel staff only].")
)
class CommentPinView(ContentObjectMixin, APIView):
    permission_classes = [IsAuthenticated,] 

    def get_object(self):
        return get_object_or_404(
                self.object.comments.select_related('user'), 
                token=self.kwargs.get("comment_token")
            )

    def post(self, request, *args, **kwargs):
        if self.object.allow_comment:
            # get the parent comment 
            comment = self.get_object()

            # parent comment channel                      
            channel = self.object.channel

            if request.user.channel_admins.filter(channel=channel):
                    comment.pinned = True if not comment.pinned else False
                    comment.save()
                    return Response("OK", status=status.HTTP_200_OK)
                    
        return Response("Permission denied.", status=status.HTTP_403_FORBIDDEN)