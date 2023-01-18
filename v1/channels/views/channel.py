from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channels.serializers.channel import (ChannelListSerializer)
from accounts.permissions import AllowAuthenticatedPermission

@extend_schema_view(
    list=extend_schema(
        description="List of channels that user is owner or admin."
    ),
)
class ChannelViewSet(ModelViewSet):
    '''A viewset for Creating, Updating, retrieving a channel'''

    permission_classes = [AllowAuthenticatedPermission,]

    def get_queryset(self):
        # TODO: union with channels that user is admin.
          return Channel.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        '''Return the appropiate'''
        if self.action == "list":
            return ChannelListSerializer

        