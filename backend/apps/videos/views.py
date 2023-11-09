from drf_spectacular.utils import extend_schema, extend_schema_view

from videos.models import Video
from videos.throttling import VideoThrottle
from videos.serializers import (
    VideoListSerializer,
    VideoCreateSerializer,
    VideoDetailSerializer,
)
from contents.views import ContentListCreateView, ContentDetailView


@extend_schema_view(
    get=extend_schema(
        description="List of a channel's videos.",
        responses={
            200: "ok",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
    post=extend_schema(
        description="Create a new video.",
        responses={
            201: "Created",
            400: "Bad request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
)
class VideoListCreateView(ContentListCreateView):
    """
    List/Create a video
    """

    throttle_classes = [VideoThrottle]
    model = Video

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VideoListSerializer

        return VideoCreateSerializer


@extend_schema_view(
    get=extend_schema(
        description="Retrieve a video.",
        responses={
            200: "ok",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
    put=extend_schema(
        description="Update a video by channel admin.",
        responses={
            200: "ok",
            400: "Bad request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
    patch=extend_schema(
        description="Update a video by channel admin.",
        responses={
            200: "ok",
            400: "Bad request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
    delete=extend_schema(
        description="Delete a video by channel admins.",
        responses={
            204: "No content",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
        },
        tags=["Videos"],
    ),
)
class VideoDetailView(ContentDetailView):
    model = Video
    throttle_classes = [VideoThrottle]
    serializer_class = VideoDetailSerializer
