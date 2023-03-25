from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channels.serializers import (ChannelListCreateSerializer, ChannelDetailSerializer)
from channels.permissions import  ChannelPermission, ChannelLimitPermission

@extend_schema_view(
    list=extend_schema(
        description="List of channels that user is owner or admin of them."
    ),
    create=extend_schema(
        description="Create a new channel [Premiums can create 10 and Normal users can create 5]."
    ),
    update=extend_schema(
        description="Update channels information [Channel staff only]."
    ),
    prtial_update=extend_schema(
        description="Update channels information [Channel staff only]."
    ),
    destroy=extend_schema(
        description="Delete a channel [Channel staff only]."
    ),
)
class ChannelViewSet(ModelViewSet):
    '''A viewset for Creating, Updating, retrieving a channel'''

    lookup_field = "token"
    filterset_fields = ['title']

    def get_permissions(self):
        '''return the appropriate permission class'''            

        if self.action in ["create"]:
            permission_classes = [ChannelLimitPermission]
        
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [ChannelPermission]
        
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request" : self.request}

    def get_queryset(self):
        # channels that user is owner of them
        owned_channel = Channel.objects.filter(owner=self.request.user)

        # channels that user is admin of them
        user_admin = self.request.user.admin.all().values("channel__id")
        channel_admin = Channel.objects.filter(id__in=user_admin)

        # return chained queryset
        return owned_channel | channel_admin

    def get_object(self):
        return get_object_or_404(Channel, token=self.kwargs["token"])


    def get_serializer_class(self):
        '''Return the appropiate serializer'''

        if self.action in ["list", "create"]:
            return ChannelListCreateSerializer
        
        elif self.action in ["retrieve", "update", "partial_update", "delete"]:
            return ChannelDetailSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @method_decorator(cache_page(5))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        
    @method_decorator(cache_page(5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)