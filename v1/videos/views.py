from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from videos.models import Video
from channels.models import ChannelAdmin
from videos.permissions import VideoPermission
from videos.serializers import VideoListSerializer, VideoCreateSeriaizer, VideoDetailSerializer


@extend_schema_view(
    list=extend_schema(
        description="List of current user's uploaded videos."
    ),
    create=extend_schema(
        description="Upload a new video [For channel that user has permission]."
    ),
    retrieve=extend_schema(
        description="Detail page of a video."
    ),
    update=extend_schema(
        description="Update a video [Users who have permission]."
    ),
    partial_update=extend_schema(
        description="Update a video [Users who have permission]."
    ),
    
)
class VideoViewSet(ModelViewSet):
    '''A viewset for adding, updating and retrieving videos'''
    lookup_field = "token"

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, VideoPermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {'user' : self.request.user}

    def get_serializer_class(self):
        if self.action == "list":
            return VideoListSerializer

        elif self.action == 'create':
            return VideoCreateSeriaizer
        
        elif self.action in ["retrieve", "update", "partial_update"]:
            return VideoDetailSerializer


    def get_queryset(self):
        '''List of users videos'''

        return Video.objects.select_related('user', 'channel')\
            .filter(user=self.request.user).order_by("-date")
    
    def get_object(self):
        video = get_object_or_404(Video.objects.select_related("channel"), 
                                    token=self.kwargs["token"])
        self.check_object_permissions(self.request, video)
        return video
    
    def update(self, request, *args, **kwargs):
        # set is_updated to True after updating the video
        object = self.get_object()
        object.is_updated = True        
        object.save()
        return super().update(request, *args, **kwargs)        