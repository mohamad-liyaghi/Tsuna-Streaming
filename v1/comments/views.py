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
)
class CommentDetailView(CommentObjectMixin, APIView):
    serializer_class = CommentDetailSerializer

    def get_object(self):
        return get_object_or_404(
            Comment.objects.select_related("parent"), content_type=self.content_type_model, 
                      object_id=self.object.id, 
                      token=self.kwargs.get("comment_token"))


    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_object()).data)
