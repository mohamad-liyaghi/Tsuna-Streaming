from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from viewers.serializers import ViewerListSerializer


@extend_schema_view(
    get=extend_schema(
        description="List of an objects viewers."
    ),
)
class ViewerListView(APIView):
    '''List of an objects viewers'''
    permission_classes = [IsAuthenticated,]

    def get(self, request, content_type_id, token, *args, **kwargs):
        content_type_model = get_object_or_404(ContentType, id=content_type_id)
        object = get_object_or_404(content_type_model.model_class(), token=token)
        serializer = ViewerListSerializer(object.viewer.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)