from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from channels.models import Channel
from channels.models import ChannelSubscriber
from channels.serializers.subscriber import SubscriberListSerializer


class SubscriberView(APIView):
    permission_classes = [IsAuthenticated,]

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        self.subscriber = ChannelSubscriber.objects.filter(channel=self.channel,
                                         user=self.request.user)

        return super().dispatch(request, *args, **kwargs)

    @method_decorator(cache_page(2))
    def get(self, request, *args, **kwargs):
        '''Check weather or not user subscribed a channel.'''

        if self.subscriber.exists():
            return Response(True, status=status.HTTP_200_OK)

        return Response(False, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Subscribe/UnSubscribe a channel.'''

        if self.subscriber:
            if request.user == self.channel.owner:
                return Response("You can not unsubscribe your own channel.", 
                                status=status.HTTP_403_FORBIDDEN)

            # if subscribed
            self.subscriber.first().delete()
            return Response("Unsubscribed successfully", status=status.HTTP_200_OK)
        
        # if hasnt subscribed
        ChannelSubscriber.objects.create(user=self.request.user, channel=self.channel)
        return Response("Subscribed successfully", status=status.HTTP_200_OK)


class SubscriberBlockView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        '''Block a user from accessing a channel [Admins only]'''

        channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        user = get_object_or_404(get_user_model(), user_id=self.kwargs["user_id"])

        if request.user == channel.owner or\
             request.user.channel_admin.filter(channel=channel, block_user=True).exists():
            
            if user.channel_admin.filter(channel=channel):
                return Response("You cant remove admins", status=status.HTTP_403_FORBIDDEN)

            subscriber = get_object_or_404(ChannelSubscriber, channel=channel,
                                            user=user)

            if subscriber.is_blocked:
                subscriber.is_blocked = False
                subscriber.save()
                return Response("User unblocked", status=status.HTTP_200_OK)

            subscriber.is_blocked = True
            subscriber.save()
            return Response("User blocked", status=status.HTTP_200_OK)

        return Response("Permission denied.", status=status.HTTP_403_FORBIDDEN)


class SubscriberListView(APIView):

    permission_classes = [IsAuthenticated,]

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel, token=self.kwargs["channel_token"])
        if request.user == self.channel.owner or\
            request.user.channel_admin.filter(channel=self.channel).exists():
            return super().dispatch(request, *args, **kwargs)

        return JsonResponse({"forbidden" : "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        if request.resolver_match.url_name == "blocked_subscriber_list":
            subscribers = ChannelSubscriber.objects\
                .select_related("channel").filter(channel=self.channel, is_blocked=True)


        else:
            subscribers = ChannelSubscriber.objects\
                .select_related("channel").filter(channel=self.channel, is_blocked=False)
            
        serializer = SubscriberListSerializer(instance=subscribers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class SubscribedChannelListView(APIView):
    '''List of channels that user subscribed'''
    permission_classes = [IsAuthenticated,]
    
    @method_decorator(cache_page(5))
    def get(self, request, *args, **kwargs):
        object = ChannelSubscriber.objects \
            .select_related("channel").filter(user=self.request.user)

        serializer = SubscriberListSerializer(instance=object, many=True)
        return Response(serializer.data)