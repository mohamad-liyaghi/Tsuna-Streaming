from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from videos.models import Video
from videos.permissions import (
    CreateVideoPermission,
    DeleteVideoPermission,
    UpdateVideoPermission,
    RetrievePrivateVideoPermission
)
from videos.throttling import VideoThrottle
from videos.serializers import (
    VideoListSerializer,
    VideoCreateSerializer,
    VideoDetailSerializer,
)
from viewers.decorators import ensure_viewer_exists
from core.mixins import ChannelObjectMixin
from core.permissions import IsChannelAdmin
from core.models import ContentVisibility


@extend_schema_view(
    get=extend_schema(
        description="List of a channel's videos.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
    post=extend_schema(
        description="Create a new video.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
)
class VideoListCreateView(ChannelObjectMixin, ListCreateAPIView):
    """
    List/Create video for a channel.
    """
    
    filterset_fields = ['title']
    throttle_classes = [VideoThrottle]

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsChannelAdmin(), CreateVideoPermission()]

        if self.request.GET.get('show_private', False):
            return [IsAuthenticated(), IsChannelAdmin()]

        return [IsAuthenticated(), ]

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {'user': self.request.user, 'channel': self.channel}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VideoListSerializer

        elif self.request.method == 'POST':
            return VideoCreateSerializer

    def get_queryset(self):
        """
        List of a channels videos
        """

        queryset = Video.objects.select_related('user', 'channel')\
            .filter(channel=self.channel).order_by("-date")
        
        if self.request.GET.get('show_private', False):
            return queryset

        return queryset.filter(visibility=ContentVisibility.PUBLISHED)
    

@extend_schema_view(    
    get=extend_schema(
        description="Retrieve a video.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
    put=extend_schema(
        description="Update a video by channel admin.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
    patch=extend_schema(
        description="Update a video by channel admin.",
        responses={
            200: 'ok',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
    delete=extend_schema(
        description="Delete a video by channel admins.",
        responses={
            204: 'No content',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Videos']
    ),
)
class VideoDetailView(ChannelObjectMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "token"
    throttle_classes = [VideoThrottle]
    serializer_class = VideoDetailSerializer

    def get_permissions(self):
        """
        Return appropriate permissions based on request method.
        """
        match self.request.method:
            case "DELETE":
                return [IsAuthenticated(), IsChannelAdmin(), DeleteVideoPermission()]
            case "PUT" | "PATCH":
                return [IsAuthenticated(), IsChannelAdmin(), UpdateVideoPermission()]
            case _:
                return [IsAuthenticated(), RetrievePrivateVideoPermission()]

    def get_object(self):
        video = get_object_or_404(
            Video.objects.select_related("channel", "user"),
            token=self.kwargs["object_token"],
            channel=self.channel
        )
        self.check_object_permissions(self.request, video)
        return video

    @ensure_viewer_exists
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
