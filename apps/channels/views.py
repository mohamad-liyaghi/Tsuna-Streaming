from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channels.serializers import (
    ChannelListCreateSerializer,
    ChannelDetailSerializer
)
from channels.permissions import ChannelPermission


@extend_schema_view(
    get=extend_schema(
        description="List of channels that user is owner or admin of them.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        tags=["Channels"]
    ),
    post=extend_schema(
        description="Create a new channel.",
        responses={
            201: 'Created',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        tags=["Channels"]
    ),
)
class ChannelListCreateView(ListCreateAPIView):
    """
    List of channels that user is owner or admin of them.
    Create a new channel [Premiums can create 10 and Normal users can create 5].
    Method: GET, POST
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = ChannelListCreateSerializer
    filterset_fields = ['title']
    
    def get_queryset(self):
        # User channels
        owned_channel = Channel.objects.filter(owner=self.request.user)

        # Get id of channels that user is admin of them
        user_admin = self.request.user.channel_admins.all().values("channel__id")
        # Get channels that user is admin of them
        channel_admin = Channel.objects.filter(id__in=user_admin)

        # return chained queryset of owned_channel and channel_admin
        return owned_channel | channel_admin
    
    def get_serializer_context(self):
        # send request to serializer
        return {"request": self.request}
    

@extend_schema_view(
    update=extend_schema(description="Update channels information [Channel staff only]."),
    prtial_update=extend_schema(description="Update channels information [Channel staff only]."),
    destroy=extend_schema(description="Delete a channel [Channel staff only]."),
)
class ChannelDetailView(RetrieveUpdateDestroyAPIView):
    '''Detail page of a channel [Retrieve, update, delete]'''
    serializer_class = ChannelDetailSerializer
    lookup_field = "token"

    def get_permissions(self):
        
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAuthenticated, ChannelPermission]
        
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        return {"request" : self.request}
    
    def get_object(self):
        return get_object_or_404(
            Channel.objects.select_related('owner'), 
            token=self.kwargs["channel_token"]
        )