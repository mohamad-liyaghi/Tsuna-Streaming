from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channels.serializers.channel import (ChannelListSerializer, ChannelCreateSerializer)
from accounts.permissions import AllowAuthenticatedPermission
from channels.permissions import ChannelLimitPermission

@extend_schema_view(
    list=extend_schema(
        description="List of channels that user is owner or admin of them."
    ),
    create=extend_schema(
        description="Create a new channel [Premiums can create 10 and Normal users can create 5]."
    ),
)
class ChannelViewSet(ModelViewSet):
    '''A viewset for Creating, Updating, retrieving a channel'''

    def get_permissions(self):
        '''return the appropriate permission class'''            
        if self.action in ["create"]:
            permission_classes = [ChannelLimitPermission]

        else:
            permission_classes = [AllowAuthenticatedPermission]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # TODO: union with channels that user is admin.
          return Channel.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        '''Return the appropiate'''
        if self.action == "list":
            return ChannelListSerializer
        
        elif self.action == "create":
            return ChannelCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

        