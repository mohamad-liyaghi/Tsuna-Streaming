from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from comments.serializers import CommentSerializer, CommentDetailSerializer
from comments.permissions import CommentPermission, CommentDetailPermission
from apps.core.mixins import ContentObjectMixin


@extend_schema_view(
    get=extend_schema(description="List an object's comments."),
    post=extend_schema(description="Add/reply to a comment if comments are allowed for an object.")
)
class CommentListCreateView(ContentObjectMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated, CommentPermission]
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        return {'user' : self.request.user, 'object' : self.object}

    def get_queryset(self):
        return self.object.comments.select_related('user').filter(parent=None).order_by("-pinned", "-date")
        


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