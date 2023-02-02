from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from comments.serializers import CommentSerializer
from comments.models import Comment


@extend_schema_view(
    get=extend_schema(
        description="List of an objects comments."
    ),
    post=extend_schema(
        description="Add a comment if comments are allowed for an object."
    ),
)
class CommentView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentSerializer


    def dispatch(self, request, *args, **kwargs):
        content_type_id = self.kwargs.get("content_type_id")
        object_token = self.kwargs.get('object_token')

        # get the content type model [eg: Video model]
        self.content_type_model = get_object_or_404(ContentType, id=content_type_id)

        # get the object
        self.object = get_object_or_404(self.content_type_model.model_class(), token=object_token)
        return super().dispatch(request, *args, **kwargs)


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