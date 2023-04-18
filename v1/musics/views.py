from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, extend_schema_view

from musics.models import Music
from musics.permissions import CreateMusicPermission
from musics.mixins import ChannelObjectMixin

from musics.serializers import (
    MusicListSerializer,
    MusicCreateSeriaizer, 
)
    

@extend_schema_view(
    get=extend_schema(
        description="List of channel's uploaded musics."
    ),
    post=extend_schema(
        description="Upload a new music [For channel that user has permission]."
    ),
)
class MusicListCreateView(ChannelObjectMixin, ListCreateAPIView):
    """
    List of musics of a channel.
    """

    filterset_fields = ['title', "visibility"]
    permission_classes = [IsAuthenticated, CreateMusicPermission]
    

    def get_queryset(self):
        """
        List of channels musics.
        Admins can also see private ones
        """

        queryset = Music.objects \
            .select_related('user', 'channel') \
            .filter(channel=self.channel) \
            .order_by("-date")

        if self.request.user.channel_admins.filter(channel=self.channel):
            return queryset

        return queryset.filter(visibility='pu')

    def get_serializer_context(self):

        return {
            'user': self.request.user,
            'channel': self.channel
        }

    def get_serializer_class(self):
        """
        Returns the serializer class based on the request method.
        """

        if self.request.method == "GET":
            return MusicListSerializer

        elif self.request.method == 'POST':
            return MusicCreateSeriaizer
