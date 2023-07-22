from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from channel_subscribers.permissions import (
    CanSubscribePermission,
    CanUnSubscribePermission
)
from channel_subscribers.serializers import SubscriberListSerializer


@extend_schema_view(
    get=extend_schema(
        description="Check wether user subscribed to a channel or not.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            404: 'Channel not found'
        },
        tags=['Subscribers']
    ),
)
class SubscriberStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the channel object from the given channel token.
        """
        return get_object_or_404(
            Channel,
            token=self.kwargs['channel_token']
        )

    def get(self, request, *args, **kwargs):
        """
        Returns whether or not a user is subscribed to a channel.
        """
        return Response(
            bool(
                ChannelSubscriber.objects.get_from_cache(
                    channel=self.get_object(),
                    user=request.user
                )
            ),
            status=status.HTTP_200_OK
        )


@extend_schema_view(
    post=extend_schema(
        description="Create a new subscriber for a channel.",
        responses={
            200: 'ok',
            401: 'Unauthorized',
            403: 'You are already subscribed to this channel.',
            404: 'Channel not found'
        },
        tags=['Subscribers']
    ),
)
class SubscriberCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanSubscribePermission]

    def get_object(self):
        """
        Returns the channel object from the given channel token.
        """
        channel = get_object_or_404(
            Channel,
            token=self.kwargs['channel_token']
        )
        self.check_object_permissions(self.request, channel)
        return channel

    def create(self, request, *args, **kwargs):
        """
        Create a new subscriber if does not exist
        """
        ChannelSubscriber.objects.create_in_cache(
            channel=self.get_object(),
            user=request.user
        )
        return Response('OK', status=status.HTTP_201_CREATED)


@extend_schema_view(
    delete=extend_schema(
        description="Delete a subscriber from channel.",
        responses={
            204: 'Deleted',
            401: 'Unauthorized',
            403: 'User hasnt subscribed yet.',
            404: 'Channel not found'
        },
        tags=['Subscribers']
    ),
)
class SubscriberDeleteView(DestroyAPIView):
    """
    Delete a Channel Subscriber for a channel
    """
    permission_classes = [IsAuthenticated, CanUnSubscribePermission]

    def get_object(self):
        """
        Returns the channel object from the given channel token.
        """
        channel = get_object_or_404(
            Channel,
            token=self.kwargs['channel_token']
        )
        self.check_object_permissions(self.request, channel)
        return channel

    def destroy(self, request, *args, **kwargs):
        ChannelSubscriber.objects.delete_in_cache(
            channel=self.get_object(),
            user=request.user
        )
        return Response(
            'ok',
            status=status.HTTP_204_NO_CONTENT
        )


@extend_schema_view(
    get=extend_schema(
        description="List of a channels subscribers.",
        responses={
            200: 'ok',
            401: 'unauthorized'
        }
    ),
)
class SubscriberListView(ListAPIView):

    serializer_class = SubscriberListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Channel, token=self.kwargs['channel_token'])

    def get_queryset(self):
        return ChannelSubscriber.objects.get_list(channel=self.get_object())
    
