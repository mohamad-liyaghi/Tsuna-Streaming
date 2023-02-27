from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from comments.serializers import CommentSerializer, CommentDetailSerializer
from comments.mixins import CommentObjectMixin
from comments.models import Comment


@extend_schema_view(
    get=extend_schema(
        description="List of an objects comments."
    ),
    post=extend_schema(
        description="Add a comment if comments are allowed for an object."
    ),
)
class CommentView(CommentObjectMixin, APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):

        comment = Comment.objects.filter(content_type=self.content_type_model, 
                            object_id=self.object.id, parent__isnull=True).order_by("-pinned", "-date")

        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        # check if comments are allowed for a post
        if self.object.allow_comment:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            serializer.save(user=request.user, content_object=self.object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response("Comments are now allowed.", status=status.HTTP_403_FORBIDDEN)


@extend_schema_view(
    get=extend_schema(
        description="Comment detail page [Replies and votes]."
    ),
    put=extend_schema(
        description="Update a comment [Only by its user]."
    ),
    delete=extend_schema(
        description="Delete a comment [by its user or channels owner]."
    ),
)
class CommentDetailView(CommentObjectMixin, APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentDetailSerializer

    def get_object(self):
        return get_object_or_404(
            Comment.objects.prefetch_related("replies", "content_object__channel"), content_type=self.content_type_model, 
                      object_id=self.object.id, 
                      token=self.kwargs.get("comment_token"))


    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_object()).data)
    
    
    def put(self, request, *args, **kwargs):

        if request.user == self.get_object().user:
            serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(edited=True)
            return Response("comment updated", status=status.HTTP_200_OK)
        
        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, *args, **kwargs):
        if request.user == self.get_object().user or \
            request.user == self.get_object().content_object.channel.owner:
            self.get_object().delete()
            return Response("Comment deleted", status=status.HTTP_200_OK)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)
    
@extend_schema_view(
    get=extend_schema(
        description="Reply a comment."
    ),
)
class CommentReplyView(CommentObjectMixin, APIView):
    permission_classes = [IsAuthenticated,] 
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        if self.object.allow_comment:
            comment = get_object_or_404(Comment, content_type=self.content_type_model, 
                      object_id=self.object.id, token=self.kwargs.get("comment_token"))

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            serializer.save(user=request.user, content_object=self.object, parent=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response("Comments are now allowed.", status=status.HTTP_403_FORBIDDEN)


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