from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from comments.serializers import CommentSerializer, CommentDetailSerializer
from comments.mixins import CommentObjectMixin
from comments.models import Comment
from comments.permissions import CommentPermission, CommentDetailPermission


@extend_schema_view(
    get=extend_schema(
        description="List of an objects comments."
    ),
    post=extend_schema(
        description="Add/Reply a comment if comments are allowed for an object."
    ),
)
class CommentListCreateView(CommentObjectMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated, CommentPermission]
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        return {'user' : self.request.user, 'object' : self.object}

    def get_queryset(self):
        return Comment.objects.filter(content_type=self.content_type_model, 
                            object_id=self.object.id, parent__isnull=True).order_by("-pinned", "-date")
        


@extend_schema_view(
    get=extend_schema(
        description="Comment detail page [Replies and votes]."
    ),
    put=extend_schema(
        description="Update a comment [Only by its user]."
    ),
    patch=extend_schema(
        description="Update a comment [Only by its user]."
    ),
    delete=extend_schema(
        description="Delete a comment [by its user or channels owner]."
    ),
)
class CommentDetailView(CommentObjectMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, CommentDetailPermission]
    serializer_class = CommentDetailSerializer

    def get_object(self):
        # self.token and self.content_type_model are in mixin        

        return get_object_or_404(
            Comment, content_type=self.content_type_model, 
                      object_id=self.object.id, 
                      token=self.kwargs.get("comment_token"))


@extend_schema_view(
    get=extend_schema(
        description="Pin a comment [Channel staff only]."
    ),
)
class CommentPinView(CommentObjectMixin, APIView):
    permission_classes = [IsAuthenticated,] 

    def post(self, request, *args, **kwargs):
        if self.object.allow_comment:
            # get the parent comment 
            comment = get_object_or_404(Comment, content_type=self.content_type_model, 
                      object_id=self.object.id, token=self.kwargs.get("comment_token"))

            # parent comment channel                      
            channel = comment.content_object.channel

            if request.user.admin.filter(channel=channel):
                        
                    comment.pinned = True if not comment.pinned else False
                    comment.save()
                    return Response(status=status.HTTP_200_OK)
                    
        return Response("Permission denied.", status=status.HTTP_403_FORBIDDEN)