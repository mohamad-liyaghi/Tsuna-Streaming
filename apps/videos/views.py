from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from videos.models import Video
from videos.permissions import VideoPermission, CreateVideoPermission
from videos.throttling import VideoThrottle
from videos.mixins import ChannelObjectMixin

from videos.serializers import (
    VideoListSerializer,
    VideoCreateSeriaizer, 
    VideoDetailSerializer
)
from viewers.decorators import ensure_viewer_exists
    

@extend_schema_view(
    get=extend_schema(
        description="List of current user's uploaded videos."
    ),
    post=extend_schema(
        description="Upload a new video [For channel that user has permission]."
    ),
)
class VideoListCreateView(ChannelObjectMixin, ListCreateAPIView):
    '''List of videos of a channel'''
    
    filterset_fields = ['title', "visibility"]
    throttle_classes = [VideoThrottle,]
    permission_classes = [IsAuthenticated, CreateVideoPermission]


    def get_serializer_context(self):
        return {'user' : self.request.user, 'channel' : self.channel}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VideoListSerializer

        elif self.request.method == 'POST':
            return VideoCreateSeriaizer
        

    def get_queryset(self):
        '''List of users videos'''

        queryset =  Video.objects.select_related('user', 'channel')\
            .filter(channel=self.channel).order_by("-date")
        
        if self.request.user.channel_admins.filter(channel=self.channel):
            return queryset

        return queryset.filter(visibility='pu')
    

@extend_schema_view(    
    get=extend_schema(
        description="Detail page of a video."
    ),
    put=extend_schema(
        description="Update a video [Users who have permission]."
    ),
    patch=extend_schema(
        description="Update a video [Users who have permission]."
    ),
    delete=extend_schema(
        description="Delete a video."
    ),
)
class VideoDetailView(ChannelObjectMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "video_token"
    permission_classes = [IsAuthenticated, VideoPermission]
    throttle_classes = [VideoThrottle,]
    serializer_class = VideoDetailSerializer

    def get_object(self):
        video = get_object_or_404(Video.objects.select_related("channel", "user"), 
                                    token=self.kwargs["video_token"], channel=self.channel)
        self.check_object_permissions(self.request, video)
        return video

    @ensure_viewer_exists
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    