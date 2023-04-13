from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channels.serializers import (ChannelListCreateSerializer, ChannelDetailSerializer)
from channels.permissions import  ChannelPermission, ChannelLimitPermission    


@extend_schema_view(
    list=extend_schema(description="List of channels that user is owner or admin of them."),
    create=extend_schema(description="Create a new channel [Premiums can create 10 and Normal users can create 5]."),
)
class ChannelListCreateView(ListCreateAPIView):
    '''List of users channels and Create channel page'''
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated, ChannelLimitPermission] if self.request.method == "POST" else [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    serializer_class = ChannelListCreateSerializer
    filterset_fields = ['title']
    
    def get_queryset(self):
        # channels that user is owner of them
        owned_channel = Channel.objects.filter(owner=self.request.user)

        # channels that user is admin of them
        user_admin = self.request.user.channel_admins.all().values("channel__id")
        channel_admin = Channel.objects.filter(id__in=user_admin)

        # return chained queryset
        return owned_channel | channel_admin
    
    def get_serializer_context(self):
        return {"request" : self.request}
    


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