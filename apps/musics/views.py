from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from contents.views import (
    ContentListCreateView,
    ContentDetailView
)
from musics.models import Music
from musics.mixins import ChannelObjectMixin
from musics.serializers import (
    MusicListSerializer,
    MusicCreateSerializer,
    MusicDetailSerializer
)
from viewers.decorators import ensure_viewer_exists


@extend_schema_view(
    get=extend_schema(
        description="List of a channel's musics.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
    post=extend_schema(
        description="Create a new music.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not found',
        },
        tags=['Musics']
    ),
)
class MusicListCreateView(ContentListCreateView):
    """
    List/Create a music
    """
    model = Music

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MusicListSerializer

        return MusicCreateSerializer


@extend_schema_view(
    get=extend_schema(description='Detail page of a music.'),
    put=extend_schema(description='Update a music [admins who have permission].'),
    patch=extend_schema(description='Update a music [admins who have permission].'),
    delete=extend_schema(description='Delete a music.')
)
class MusicDetailView(ChannelObjectMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'music_token'
    permission_classes = [IsAuthenticated,]
    serializer_class = MusicDetailSerializer

    def get_object(self):
        music = get_object_or_404(
            Music.objects.select_related('channel', 'user'), 
            token=self.kwargs['music_token'], channel=self.channel
        )
        self.check_object_permissions(self.request, music)
        return music

    @ensure_viewer_exists
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)