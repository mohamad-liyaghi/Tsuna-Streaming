from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from channel_subscribers.permissions import SubscriberPermission
from channel_subscribers.serializers import SubscriberListSerializer


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


@extend_schema_view(
    get=extend_schema(
        description="List of subscribers of a channel."
    ),
)
class SubscriberListView(ListAPIView):

    serializer_class = SubscriberListSerializer

    def get_queryset(self):

        subscriber_keys = cache.keys(f'subscriber:{self.kwargs["channel_token"]}:*')

        subscribers_in_database = list(ChannelSubscriber.objects.filter(channel__token=self.kwargs['channel_token']))

        subscribers_in_cache = [
            {
                "user": key.split(":")[2],
                "date": cache_value.get('date', None),
                "source": cache_value['source']
            }

            for key in subscriber_keys
            if (cache_value := cache.get(key)) and
            # get those subscribers that are only in cache and they are marked as subscribed
            cache_value['source'] == 'cache' and
            cache_value.get('subscription_status') == 'subscribed'
        ]

        return subscribers_in_cache + subscribers_in_database
    
