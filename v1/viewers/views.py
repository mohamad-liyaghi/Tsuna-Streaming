from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from viewers.serializers import ViewerListSerializer
from core.mixins import ContentObjectMixin

@extend_schema_view(
    get=extend_schema(description="List of an objects viewers."),
)
class ViewerListView(ContentObjectMixin ,APIView):
    '''List of an objects viewers'''
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        serializer = ViewerListSerializer(self.object.viewers.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)