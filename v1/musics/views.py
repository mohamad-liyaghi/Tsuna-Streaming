from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from musics.models import Music
from musics.permissions import CreateMusicPermission, MusicDetailPermission
from musics.mixins import ChannelObjectMixin
from musics.serializers import (MusicListSerializer, MusicCreateSeriaizer, 
                                MusicDetailSerializer)
from viewers.decorators import check_viewer_status
    

@extend_schema_view(
    get=extend_schema(description="List of channel's uploaded musics."),
    post=extend_schema(description="Upload a new music [For channel that user has permission].")
)
class MusicListCreateView(ChannelObjectMixin, ListCreateAPIView):
    filterset_fields = ['title', 'visibility']
    permission_classes = [IsAuthenticated, CreateMusicPermission]
    

    def get_queryset(self):
        """
        List of channels musics.
        Admins can also see private ones
        """

    def get_queryset(self):
        queryset = Music.objects.select_related('user', 'channel').filter(channel=self.channel).order_by('-date')
        if self.request.user.channel_admins.filter(channel=self.channel):
            return queryset
        return queryset.filter(visibility='pu')

    def get_serializer_context(self):

        return {
            'user': self.request.user,
            'channel': self.channel
        }

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MusicListSerializer

        elif self.request.method == 'POST':
            return MusicCreateSeriaizer


@extend_schema_view(
    get=extend_schema(description='Detail page of a music.'),
    put=extend_schema(description='Update a music [admins who have permission].'),
    patch=extend_schema(description='Update a music [admins who have permission].'),
    delete=extend_schema(description='Delete a music.')
)
class MusicDetailView(ChannelObjectMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = 'music_token'
    permission_classes = [IsAuthenticated, MusicDetailPermission]
    serializer_class = MusicDetailSerializer

    def get_object(self):
        music = get_object_or_404(
            Music.objects.select_related('channel', 'user'), 
            token=self.kwargs['music_token'], channel=self.channel
        )
        self.check_object_permissions(self.request, music)
        return music

    @check_viewer_status # This decorator adds viewer for the object if not already exist
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)