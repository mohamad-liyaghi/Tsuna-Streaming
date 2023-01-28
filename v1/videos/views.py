from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from videos.models import Video
from videos.serializers import VideoListSerializer


@extend_schema_view(
    list=extend_schema(
        description="List of current user's uploaded videos."
    ),
)
class VideoViewSet(ModelViewSet):
    '''A viewset for adding, updating and retrieving videos'''

    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == "list":
            return VideoListSerializer


    def get_queryset(self):
        '''List of users videos'''
        
        return Video.objects.select_related('user', 'channel')\
            .filter(user=self.request.user).order_by("-date")