from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from channel_subscribers.permissions import SubscriberPermission


@extend_schema_view(
    get=extend_schema(
        description="Check wether user subscribed to a channel or not."
    ),
    post=extend_schema(
        description="Subscribe to a channel."
    ),
    delete=extend_schema(
        description="Unsubscribe from a channel."
    ),
)
class SubscriberView(APIView):
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated, SubscriberPermission]

    def dispatch(self, request, *args, **kwargs):
        # Check if the given channel exists
        self.channel = get_object_or_404(Channel, token=self.kwargs['channel_token'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, channel_token, *args, **kwargs):
        '''
        Returns whether or not a user is subscribed to a channel.
        '''

        # Get the subscription status from the database and cache
        subscriber = ChannelSubscriber.objects.get_from_cache(channel_token, request.user.token)

        # Return True if subscribed, else return False
        return Response(True if subscriber else False, status=status.HTTP_200_OK)
    

    def post(self, request, channel_token, *args, **kwargs):
        '''
        Creates a new subscriber and saves it into the cache. Then, Celery inserts it into the database.
        If the user has already subscribed to the channel, the permission class prevents them from performing this action. 
        '''

        ChannelSubscriber.objects.subscribe_in_cache(
            channel_token=channel_token, user_token=request.user.token
        )
        return Response('OK', status=status.HTTP_201_CREATED)


    def delete(self, request, channel_token, *args, **kwargs):
        '''
        Removes the subscriber record from the cache and marks the user as unsubscribed from the channel.
        Then, Celery deletes the subscriber from the database.
        If the user hasn't subscribed to the channel yet, the permission class prevents them from performing this action.
        '''

        # Delete the subscriber
        ChannelSubscriber.objects.unsubscribe_in_cache(
            channel_token=channel_token, user_token=request.user.token
        )  
        
        return Response('OK', status=status.HTTP_204_NO_CONTENT)
