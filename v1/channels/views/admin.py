from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.serializers.admin import ChannelAdminListSerializer, ChannelAdminCreateSerializer, ChannelAdminDetailSerializer
from channels.models import Channel, ChannelAdmin, ChannelSubscriber
from channels.permissions import ChannelAdminPermission, ChannelAdminDetailPermission


@extend_schema_view(
    get=extend_schema(
        description="List of admins of a channel."
    ),
    post=extend_schema(
        description="Add a new admin to a channel."
    ),
)
class ChannelAdminView(ListCreateAPIView):
    '''Get channel admins and add an admin'''

    permission_classes = [IsAuthenticated, ChannelAdminPermission] 
    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, token=self.kwargs["token"])
        return super().dispatch(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChannelAdminListSerializer

        elif self.request.method == "POST":
            return ChannelAdminCreateSerializer

    def get_queryset(self):    
        return ChannelAdmin.objects.select_related(
                                        "channel", "channel__owner"
                                    ).filter(channel=self.channel)


    def post(self, request, *args, **kwargs):
        '''Create a new admin [Admins who have permission]'''

        serializer = ChannelAdminCreateSerializer(data=request.data)  

        if serializer.is_valid():
            serializer.save(promoted_by=request.user, channel=self.channel)
            return Response("Admin added.", status=status.HTTP_201_CREATED)    

        return Response("Invalid information", status=status.HTTP_400_BAD_REQUEST)

        
    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        '''List of admins of a channel [Admins]'''
        return super().get(request, *args, **kwargs)



@extend_schema_view(
    get=extend_schema(
        description="Admin permission list, [Admin and channel owner]."
    ),
    put=extend_schema(
        description="Update an admins permission, [Channel owner]."
    ),
    patch=extend_schema(
        description="Update an admins permission, [Channel owner]."
    ),
    destroy=extend_schema(
        description="Delete an admin, [Channel owner]."
    ),
)
class ChannelAdminDetailView(RetrieveUpdateDestroyAPIView):
    '''Detail page of admins'''

    serializer_class = ChannelAdminDetailSerializer
    permission_classes = [IsAuthenticated, ChannelAdminDetailPermission]
    
    def get_queryset(self):
        return Channel.objects.filter(token=self.kwargs["channel_token"])


    def get_object(self):
        channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        admin = get_object_or_404(ChannelAdmin, channel=channel, token=self.kwargs["admin_token"])

        if self.request.user == channel.owner or \
                 self.request.user == admin.user:
            return admin

        raise Http404("No result found.")
    
    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)